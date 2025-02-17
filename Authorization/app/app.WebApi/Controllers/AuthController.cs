using System.Data;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using app.Application.Services;
using app.Core.Models;
using app.Core.Models.Response;
using app.Infrastructure;
using FluentValidation;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace app.WebApi.Controllers
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
		[FromServices] IValidator<RevokeTokenModel> revokeTokenModelValidator,
		[FromServices] AuthService authService
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

		private readonly AuthService _authService = authService;

		[HttpPost("register")]
		public async Task<IActionResult> Register([FromBody] RegisterModel model)
		{
			var result = await _authService.RegisterAsync(model);

			return result.Success
				? ResponseHelper.Ok(result.Data, result.StatusCode)
				: ResponseHelper.Error(result.StatusCode);
		}

		[HttpPost("login")]
		public async Task<IActionResult> Login([FromBody] LoginModel model)
		{
			var result = await _authService.LoginAsync(model);

			return result.Success
				? ResponseHelper.Ok(result.Data, result.StatusCode)
				: ResponseHelper.Error(result.StatusCode);
		}

		[HttpPost("refresh-token")]
		public async Task<IActionResult> RefreshToken([FromBody] RefreshTokenModel model)
		{
			var result = await _authService.RefreshTokenAsync(model);

			return result.Success
				? ResponseHelper.Ok(result.Data, result.StatusCode)
				: ResponseHelper.Error(result.StatusCode);
		}

		[HttpPost("revoke-token")]
		public async Task<IActionResult> RevokeToken([FromBody] RevokeTokenModel model)
		{
			var result = await _authService.RevokeTokenAsync(model);

			return result.Success
				? ResponseHelper.Ok(result.Data, result.StatusCode)
				: ResponseHelper.Error(result.StatusCode);
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

			var result = await _authService.LogoutAsync(userId);

			return result.Success
				? ResponseHelper.Ok(result.Data, result.StatusCode)
				: ResponseHelper.Error(result.StatusCode);
		}
	}
}