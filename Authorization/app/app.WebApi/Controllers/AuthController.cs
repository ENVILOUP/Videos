using System.Data;
using System.IdentityModel.Tokens.Jwt;
using System.Security.Claims;
using app.Application.DTOs;
using app.Application.Services;
using app.Core.Models;
using app.Infrastructure;
using app.WebApi.Helpers.Response;
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
		[FromServices] AuthService authService
		) : ControllerBase
	{
		private readonly AuthService _authService = authService;

		[HttpPost("register")]
		public async Task<IActionResult> Register([FromBody] RegisterModel model)
		{
			var result = await _authService.RegisterAsync(model);

			return result.Success
				? ResponseHelper.Ok(result.Data, result.StatusCode)
				: ResponseHelper.Error(result.StatusCode);
		}

		[Authorize(Policy = "RequireAdminRole")]
		[HttpPost("create-user")]
		public async Task<IActionResult> CreateUser([FromBody] CreateUserModel model)
		{
			var result = await _authService.CreateUserAsync(model);

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