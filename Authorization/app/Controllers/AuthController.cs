using System;
using System.Collections.Generic;
using System.Data;
using System.Linq;
using System.Security.Claims;
using System.Threading.Tasks;
using app.Models;
using app.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace app.Controllers
{
	[ApiController]
	[Route("api/[controller]")]
	public class AuthController([FromServices] UserManager<IdentityUser> userManager, [FromServices] JWTService jwtService, [FromServices] AppDbContext dbContext, ILogger<AuthController> logger, [FromServices] IConfiguration configuration) : ControllerBase
	{
		private readonly UserManager<IdentityUser> _userManager = userManager;
		private readonly JWTService _jwtService = jwtService;
		private readonly AppDbContext _dbContext = dbContext;
		private readonly ILogger<AuthController> _logger = logger;
		private readonly IConfiguration _configuration = configuration;

		[HttpPost("register")]
		public async Task<IActionResult> Register([FromBody] RegisterModel model)
		{
			if (!ModelState.IsValid)
			{
				return BadRequest(ModelState);
			}

			var user = new IdentityUser { UserName = model.Username, Email = model.Email };
			var result = await _userManager.CreateAsync(user, model.Password);

			if (!result.Succeeded)
			{
				return BadRequest(result.Errors);
			}

			return Ok();
		}

		[HttpPost("login")]
		public async Task<IActionResult> Login([FromBody] LoginModel model)
		{
			if (!ModelState.IsValid)
			{
				return BadRequest(ModelState);
			}

			var user = await _userManager.FindByNameAsync(model.Username);

			if (user == null)
			{
				return Unauthorized(new { message = "User not found" });
			}

			if (!await _userManager.CheckPasswordAsync(user, model.Password))
			{
				return Unauthorized(new { message = "Invalid password" });
			}

			var accessToken = _jwtService.GenerateJwtToken(user);
			var refreshToken = _jwtService.GenerateRefreshToken();

			var refreshTokenEntity = GetNewRefreshToken(user, refreshToken);

			await _dbContext.RefreshTokens.AddAsync(refreshTokenEntity);
			await _dbContext.SaveChangesAsync();

			return Ok(new { AccessToken = accessToken, RefreshToken = refreshToken });
		}

		[HttpPost("refresh-token")]
		public async Task<IActionResult> RefreshToken([FromBody] RefreshTokenModel model)
		{
			if (!ModelState.IsValid)
			{
				return BadRequest(ModelState);
			}

			var refreshToken = await _dbContext.RefreshTokens.FirstOrDefaultAsync(refreshToken => refreshToken.Token == model.RefreshToken);

			if (refreshToken == null)
			{
				return Unauthorized(new { message = "Invalid refresh token" });
			}

			const int WINDOW_TIME_HOURS = 1;
			var tokenExpiryWithWindow = refreshToken.ExpiryDate.AddHours(WINDOW_TIME_HOURS);

			if (tokenExpiryWithWindow <= DateTime.UtcNow || refreshToken.IsRevoked || refreshToken.IsUsed)
			{
				return Unauthorized(new { message = "Invalid or expired refresh token" });
			}

			var user = await _userManager.FindByIdAsync(refreshToken.UserId);
			if (user == null)
			{
				return Unauthorized(new { message = "User not found" });
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

			return Ok(new { AccessToken = newAccessToken, RefreshToken = newRefreshToken });
		}

		[HttpPost("revoke-token")]
		public async Task<IActionResult> RevokeToken([FromBody] RevokeTokenModel model)
		{
			if (!ModelState.IsValid)
			{
				return BadRequest(ModelState);
			}

			var refreshToken = await _dbContext.RefreshTokens.FirstOrDefaultAsync(refreshToken => refreshToken.Token == model.RefreshToken);

			if (refreshToken == null)
			{
				return BadRequest(new { message = "Invalid refresh token" });
			}

			if (refreshToken.IsRevoked)
			{
				return BadRequest(new { message = "Refresh token has already been revoked" });
			}

			refreshToken.IsRevoked = true;

			_dbContext.RefreshTokens.Update(refreshToken);
			await _dbContext.SaveChangesAsync();

			return Ok(new { message = "Refresh token revoked successfully" });
		}

		[Authorize]
		[HttpPost("logout")]
		public async Task<IActionResult> Logout()
		{
			var userId = User.FindFirstValue(ClaimTypes.NameIdentifier);
			if (userId == null)
			{
				return BadRequest(new { message = "User not found" });
			}

			var tokens = _dbContext.RefreshTokens.Where(refreshToken => refreshToken.UserId == userId).ToList();

			tokens.ForEach(refreshToken => refreshToken.IsRevoked = true);
			_dbContext.RefreshTokens.UpdateRange(tokens);

			await _dbContext.SaveChangesAsync();

			return Ok(new { message = "Logout successful" });
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