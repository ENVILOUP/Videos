using app.Application.DTOs;
using app.Application.Entities;
using app.Core.IRepositories;
using app.Core.Models;
using app.Infrastructure;
using FluentValidation;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;

namespace app.Application.Services
{
	public class AuthService(
		[FromServices] UserManager<IdentityUser> userManager,
		[FromServices] JWTService jwtService,
		[FromServices] ILogger<AuthService> logger,
		[FromServices] IConfiguration configuration,
		[FromServices] IValidator<RegisterModel> registerModelValidator,
		[FromServices] IValidator<LoginModel> loginModelValidator,
		[FromServices] IValidator<RefreshTokenModel> refreshTokenModelValidator,
		[FromServices] IValidator<RevokeTokenModel> revokeTokenModelValidator,
		[FromServices] IAuthRepository authRepository,
		[FromServices] AppDbContext dbContext
	)
	{
		private readonly UserManager<IdentityUser> _userManager = userManager;
		private readonly JWTService _jwtService = jwtService;
		private readonly ILogger<AuthService> _logger = logger;
		private readonly IConfiguration _configuration = configuration;
		private readonly IValidator<RegisterModel> _registerModelValidator = registerModelValidator;
		private readonly IValidator<LoginModel> _loginModelValidator = loginModelValidator;
		private readonly IValidator<RefreshTokenModel> _refreshTokenModelValidator = refreshTokenModelValidator;
		private readonly IValidator<RevokeTokenModel> _revokeTokenModelValidator = revokeTokenModelValidator;

		private readonly IAuthRepository _authRepository = authRepository;
		private readonly AppDbContext _dbContext = dbContext;

		public async Task<ServiceResult<string>> RegisterAsync(RegisterModel model)
		{
			var validationResult = await _registerModelValidator.ValidateAsync(model);
			if (!validationResult.IsValid)
			{
				_logger.LogError(validationResult.Errors.ToString());
				return ServiceResult<string>.Fail(AuthResponseStatusCode.RegisterNotValidData);
			}

			var user = new IdentityUser { UserName = model.Username, Email = model.Email };

			try
			{
				var result = await _authRepository.AddNewUser(user, model.Password);

				if (!result.Succeeded)
				{
					_logger.LogError(result.Errors.ToString());
					return ServiceResult<string>.Fail(AuthResponseStatusCode.RegistrationFailed);
				}

			}
			catch (Exception ex)
			{
				_logger.LogError(ex, message: ex.Message);
				return ServiceResult<string>.Fail(AuthResponseStatusCode.ServerError);
			}

			return ServiceResult<string>.Ok(user.Id, AuthResponseStatusCode.Registered);
		}

		public async Task<ServiceResult<TokensModel>> LoginAsync(LoginModel model)
		{
			var validationResult = await _loginModelValidator.ValidateAsync(model);
			if (!validationResult.IsValid)
			{
				_logger.LogError(validationResult.Errors.ToString());
				return ServiceResult<TokensModel>.Fail(AuthResponseStatusCode.LoginNotValidData);
			}

			var user = await _userManager.FindByNameAsync(model.Username);

			if (user == null)
			{
				_logger.LogError("User not found");
				return ServiceResult<TokensModel>.Fail(AuthResponseStatusCode.UserNotFound);
			}

			if (!await _userManager.CheckPasswordAsync(user, model.Password))
			{
				_logger.LogError("Login not match password");
				return ServiceResult<TokensModel>.Fail(AuthResponseStatusCode.LoginNotMatchPassword);
			}

			var accessToken = _jwtService.GenerateJwtToken(user);
			var refreshToken = _jwtService.GenerateRefreshToken();

			var refreshTokenEntity = GetNewRefreshToken(user, refreshToken);

			try
			{
				await _authRepository.AddRefreshToken(refreshTokenEntity);
			}
			catch (Exception ex)
			{
				_logger.LogError(ex, message: ex.Message);
				return ServiceResult<TokensModel>.Fail(AuthResponseStatusCode.ServerError);
			}

			var tokens = new TokensModel
			{
				AccessToken = accessToken,
				RefreshToken = refreshToken
			};

			return ServiceResult<TokensModel>.Ok(tokens, AuthResponseStatusCode.LoggedIn);
		}

		public async Task<ServiceResult<TokensModel>> RefreshTokenAsync(RefreshTokenModel model)
		{
			var validationResult = await _refreshTokenModelValidator.ValidateAsync(model);
			if (!validationResult.IsValid)
			{
				_logger.LogError(validationResult.Errors.ToString());
				return ServiceResult<TokensModel>.Fail(AuthResponseStatusCode.RefreshTokenNotValidData);
			}

			var refreshToken = await _dbContext.RefreshTokens.FirstOrDefaultAsync(refreshToken => refreshToken.Token == model.RefreshToken);

			if (refreshToken == null)
			{
				_logger.LogError("Refresh token not found");
				return ServiceResult<TokensModel>.Fail(AuthResponseStatusCode.RefreshTokenNotFound);
			}

			const int WINDOW_TIME_HOURS = 1;
			var tokenExpiryWithWindow = refreshToken.ExpiryDate.AddHours(WINDOW_TIME_HOURS);

			if (tokenExpiryWithWindow <= DateTime.UtcNow || refreshToken.IsRevoked || refreshToken.IsUsed)
			{
				_logger.LogError("Invalid token");
				return ServiceResult<TokensModel>.Fail(AuthResponseStatusCode.InvalidToken);
			}

			var user = await _userManager.FindByIdAsync(refreshToken.UserId);
			if (user == null)
			{
				_logger.LogError("User not found");
				return ServiceResult<TokensModel>.Fail(AuthResponseStatusCode.UserNotFound);
			}

			var newAccessToken = _jwtService.GenerateJwtToken(user);
			var newRefreshToken = model.RefreshToken;

			if (refreshToken.ExpiryDate <= DateTime.UtcNow)
			{
				newRefreshToken = _jwtService.GenerateRefreshToken();
				var newRefreshTokenEntity = GetNewRefreshToken(user, newRefreshToken);

				try
				{
					await _authRepository.UpdateRefreshToken(
						newRefreshTokenEntity: newRefreshTokenEntity,
						oldRefreshTokenEntity: refreshToken
					);
				}
				catch (Exception ex)
				{
					_logger.LogError(ex, message: ex.Message);
					return ServiceResult<TokensModel>.Fail(AuthResponseStatusCode.ServerError);
				}
			}

			var tokens = new TokensModel
			{
				AccessToken = newAccessToken,
				RefreshToken = newRefreshToken
			};

			return ServiceResult<TokensModel>.Ok(tokens, AuthResponseStatusCode.TokenRefreshed);
		}

		public async Task<ServiceResult<string>> RevokeTokenAsync(RevokeTokenModel model)
		{
			var validationResult = await _revokeTokenModelValidator.ValidateAsync(model);
			if (!validationResult.IsValid)
			{
				_logger.LogError(validationResult.Errors.ToString());
				return ServiceResult<string>.Fail(AuthResponseStatusCode.RevokeTokenNotValidData);
			}

			var refreshToken = await _dbContext.RefreshTokens.FirstOrDefaultAsync(refreshToken => refreshToken.Token == model.RefreshToken);

			if (refreshToken == null)
			{
				_logger.LogError("Refresh token not found");
				return ServiceResult<string>.Fail(AuthResponseStatusCode.RefreshTokenNotFound);
			}

			if (refreshToken.IsRevoked)
			{
				_logger.LogError("Token already revoked");
				return ServiceResult<string>.Fail(AuthResponseStatusCode.TokenAlreadyRevoked);
			}

			try
			{
				await _authRepository.RevokeRefreshToken(refreshToken);
			}
			catch (Exception ex)
			{
				_logger.LogError(ex, message: ex.Message);
				return ServiceResult<string>.Fail(AuthResponseStatusCode.ServerError);
			}

			return ServiceResult<string>.Ok(refreshToken.Id.ToString(), AuthResponseStatusCode.TokenRevoked);
		}

		public async Task<ServiceResult<string>> LogoutAsync(string userId)
		{
			var tokens = _dbContext.RefreshTokens.Where(refreshToken => refreshToken.UserId == userId).ToList();

			try
			{
				await _authRepository.UserLogout(tokens);
			}
			catch (Exception ex)
			{
				_logger.LogError(ex, message: ex.Message);
				return ServiceResult<string>.Fail(AuthResponseStatusCode.ServerError);
			}

			return ServiceResult<string>.Ok(userId, AuthResponseStatusCode.LoggedOut);
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