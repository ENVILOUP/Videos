using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using app.Models;
using app.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;

namespace app.Controllers
{
	[ApiController]
	[Route("api/[controller]")]
	public class AuthController([FromServices] UserManager<IdentityUser> userManager, [FromServices] JWTService jwtService) : ControllerBase
	{
		private readonly UserManager<IdentityUser> _userManager = userManager;
		private readonly JWTService _jwtService = jwtService;

		[HttpPost("register")]
		public async Task<IActionResult> Register([FromBody] RegisterModel model)
		{
			var user = new IdentityUser { UserName = model.Username, Email = model.Email };
			var result = await _userManager.CreateAsync(user, model.Password);

			if (!result.Succeeded)
			{
				return BadRequest(result.Errors);
			}

			var token = _jwtService.GenerateJwtToken(user);
			return Ok(new { Token = token });
		}

		[HttpPost("login")]
		public async Task<IActionResult> Login([FromBody] LoginModel model)
		{
			var user = await _userManager.FindByNameAsync(model.Username);

			if (user == null) return Unauthorized();
			if (!await _userManager.CheckPasswordAsync(user, model.Password)) return Unauthorized();

			var token = _jwtService.GenerateJwtToken(user);
			return Ok(new { Token = token });
		}
	}
}