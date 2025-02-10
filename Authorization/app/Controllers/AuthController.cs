using System;
using System.Collections.Generic;
using System.Data;
using System.IdentityModel.Tokens.Jwt;
using System.Linq;
using System.Security.Claims;
using System.Threading.Tasks;
using app.Models;
using app.Models.Response;
using app.Services;
using FluentValidation;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Http.Headers;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace app.Controllers
{
	[ApiController]
	[Route("api/[controller]")]
	public class AuthController(
		[FromServices] UserManager<IdentityUser> userManager,
		[FromServices] JWTService jwtService,
		[FromServices] AppDbContext dbContext,
		ILogger<AuthController> logger,
		[FromServices] IConfiguration configuration,
		[FromServices] IValidator<RegisterModel> registerModelValidator,
		[FromServices] IValidator<LoginModel> loginModelValidator,
		[FromServices] IValidator<RefreshTokenModel> refreshTokenModelValidator,
		[FromServices] IValidator<RevokeTokenModel> revokeTokenModelValidator
		) : ControllerBase
	{
		private readonly UserManager<IdentityUser> _userManager = userManager;
		private readonly JWTService _jwtService = jwtService;
		private readonly AppDbContext _dbContext = dbContext;
		private readonly ILogger<AuthController> _logger = logger;
		private readonly IConfiguration _configuration = configuration;
		private readonly IValidator<RegisterModel> _registerModelValidator = registerModelValidator;
		private readonly IValidator<LoginModel> _loginModelValidator = loginModelValidator;
		private readonly IValidator<RefreshTokenModel> _refreshTokenModelValidator = refreshTokenModelValidator;
		private readonly IValidator<RevokeTokenModel> _revokeTokenModelValidator = revokeTokenModelValidator;

		[HttpPost("register")]
		public async Task<IActionResult> Register([FromBody] RegisterModel model)
		{
			var validationResult = await _registerModelValidator.ValidateAsync(model);
			if (!validationResult.IsValid)
			{
				return ResponseHelper.Error(AuthResponseStatusCode.RegisterNotValidData);
			}

			var user = new IdentityUser { UserName = model.Username, Email = model.Email };
			var result = await _userManager.CreateAsync(user, model.Password);

			if (!result.Succeeded)
			{
				return ResponseHelper.Error(AuthResponseStatusCode.RegistrationFailed);
			}

			return ResponseHelper.Ok(user.Id, AuthResponseStatusCode.Registered);
		}

		[HttpPost("login")]
		public async Task<IActionResult> Login([FromBody] LoginModel model)
		{
			var validationResult = await _loginModelValidator.ValidateAsync(model);
			if (!validationResult.IsValid)
			{
				return ResponseHelper.Error(AuthResponseStatusCode.LoginNotValidData);
			}

			var user = await _userManager.FindByNameAsync(model.Username);

			if (user == null)
			{
				return ResponseHelper.Error(AuthResponseStatusCode.UserNotFound);
			}

			if (!await _userManager.CheckPasswordAsync(user, model.Password))
			{
				return ResponseHelper.Error(AuthResponseStatusCode.LoginNotMatchPassword);
			}

			var accessToken = _jwtService.GenerateJwtToken(user);
			var refreshToken = _jwtService.GenerateRefreshToken();

			var refreshTokenEntity = GetNewRefreshToken(user, refreshToken);

			await _dbContext.RefreshTokens.AddAsync(refreshTokenEntity);
			await _dbContext.SaveChangesAsync();

			return ResponseHelper.Ok(new { AccessToken = accessToken, RefreshToken = refreshToken }, AuthResponseStatusCode.LoggedIn);
		}

		[HttpPost("refresh-token")]
		public async Task<IActionResult> RefreshToken([FromBody] RefreshTokenModel model)
		{
			var validationResult = await _refreshTokenModelValidator.ValidateAsync(model);
			if (!validationResult.IsValid)
			{
				return ResponseHelper.Error(AuthResponseStatusCode.RefreshTokenNotValidData);
			}

			var refreshToken = await _dbContext.RefreshTokens.FirstOrDefaultAsync(refreshToken => refreshToken.Token == model.RefreshToken);

			if (refreshToken == null)
			{
				return ResponseHelper.Error(AuthResponseStatusCode.RefreshTokenNotFound);
			}

			const int WINDOW_TIME_HOURS = 1;
			var tokenExpiryWithWindow = refreshToken.ExpiryDate.AddHours(WINDOW_TIME_HOURS);

			if (tokenExpiryWithWindow <= DateTime.UtcNow || refreshToken.IsRevoked || refreshToken.IsUsed)
			{
				return ResponseHelper.Error(AuthResponseStatusCode.InvalidToken);
			}

			var user = await _userManager.FindByIdAsync(refreshToken.UserId);
			if (user == null)
			{
				return ResponseHelper.Error(AuthResponseStatusCode.UserNotFound);
			}

			var newAccessToken = _jwtService.GenerateJwtToken(user);
			var newRefreshToken = model.RefreshToken;

			if (refreshToken.ExpiryDate <= DateTime.UtcNow)
			{
				using var transaction = _dbContext.Database.BeginTransaction();

				newRefreshToken = _jwtService.GenerateRefreshToken();
				var newRefreshTokenEntity = GetNewRefreshToken(user, newRefreshToken);
				await _dbContext.RefreshTokens.AddAsync(newRefreshTokenEntity);

				refreshToken.IsUsed = true;
				_dbContext.RefreshTokens.Update(refreshToken);
				await _dbContext.SaveChangesAsync();

				await transaction.CommitAsync();
			}

			return ResponseHelper.Ok(new { AccessToken = newAccessToken, RefreshToken = newRefreshToken }, AuthResponseStatusCode.TokenRefreshed);
		}

		[HttpPost("revoke-token")]
		public async Task<IActionResult> RevokeToken([FromBody] RevokeTokenModel model)
		{
			var validationResult = await _revokeTokenModelValidator.ValidateAsync(model);
			if (!validationResult.IsValid)
			{
				return ResponseHelper.Error(AuthResponseStatusCode.RevokeTokenNotValidData);
			}

			var refreshToken = await _dbContext.RefreshTokens.FirstOrDefaultAsync(refreshToken => refreshToken.Token == model.RefreshToken);

			if (refreshToken == null)
			{
				return ResponseHelper.Error(AuthResponseStatusCode.RefreshTokenNotFound);
			}

			if (refreshToken.IsRevoked)
			{
				return ResponseHelper.Error(AuthResponseStatusCode.TokenAlreadyRevoked);
			}

			refreshToken.IsRevoked = true;

			_dbContext.RefreshTokens.Update(refreshToken);
			await _dbContext.SaveChangesAsync();

			return ResponseHelper.Ok(refreshToken.Id, AuthResponseStatusCode.TokenRevoked);
		}

		[Authorize]
		[HttpPost("logout")]
		public async Task<IActionResult> Logout()
		{
			var userId = User.FindFirstValue(JwtRegisteredClaimNames.Sub);
			if (userId == null)
			{
				return ResponseHelper.Error(AuthResponseStatusCode.UserNotFound);
			}

			var tokens = _dbContext.RefreshTokens.Where(refreshToken => refreshToken.UserId == userId).ToList();

			tokens.ForEach(refreshToken => refreshToken.IsRevoked = true);
			_dbContext.RefreshTokens.UpdateRange(tokens);

			await _dbContext.SaveChangesAsync();

			return ResponseHelper.Ok(userId, AuthResponseStatusCode.LoggedOut);
		}

		private RefreshToken GetNewRefreshToken(IdentityUser user, string newRefreshToken)
		{
			var expiresValue = _configuration.GetSection("JWT:RefreshTokenExpirationDays").Value;

			if (string.IsNullOrEmpty(expiresValue))
			{
				throw new InvalidOperationException("JWT:RefreshTokenExpirationDays not found");
			}

			var currentDateTimeUtc = DateTime.UtcNow;
			var expiryDateUtc = currentDateTimeUtc.AddDays(Convert.ToDouble(expiresValue));

			return new RefreshToken
			{
				Token = newRefreshToken,
				UserId = user.Id,
				ExpiryDate = DateTime.SpecifyKind(expiryDateUtc, DateTimeKind.Utc),
			};
		}
	}
}