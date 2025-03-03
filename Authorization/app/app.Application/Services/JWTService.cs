using System;
using System.Collections.Generic;
using System.IdentityModel.Tokens.Jwt;
using System.Linq;
using System.Security.Claims;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;
using app.Application.IRepositories;
using app.Core.Models;
using Microsoft.AspNetCore.Identity;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using Microsoft.IdentityModel.Tokens;

namespace app.Application.Services
{
    public class JWTService(IConfiguration configuration, ILogger<JWTService> logger, IUserRepository userRepository)
    {
		private readonly IConfiguration _configuration = configuration;
		private readonly ILogger<JWTService> _logger = logger;
		private readonly IUserRepository _userRepository = userRepository;

        public async Task<string> GenerateJwtToken(IdentityUser user)
		{
			var jtiId = Guid.NewGuid().ToString();
			var userRole = await _userRepository.GetUserRole(user);

			var claims = new[]
			{
				new Claim(JwtRegisteredClaimNames.Sub, user.Id),
				new Claim("role", userRole),
				new Claim(JwtRegisteredClaimNames.Jti, jtiId),
			};

			string jwtKey = _configuration["JWT_KEY"] ?? throw new InvalidOperationException("JWT_Key not found");

			if (string.IsNullOrEmpty(jwtKey))
			{
				throw new InvalidOperationException("JWT_Key not found");
			}

			var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(jwtKey));

			var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

			var expiresValue = _configuration.GetSection("JWT").GetValue<int>("AccessTokenExpirationMinutes");

			if (expiresValue == 0)
			{
				throw new InvalidOperationException("JWT:AccessTokenExpirationMinutes not found");
			}

			var token = new JwtSecurityToken(
				issuer: _configuration.GetSection("JWT:Issuer")?.Value ?? throw new InvalidOperationException("JWT:Issuer not found"),
				audience: _configuration.GetSection("JWT:Audience")?.Value ?? throw new InvalidOperationException("JWT:Audience not found"),
				claims: claims,
				expires: DateTime.UtcNow.AddMinutes(Convert.ToDouble(expiresValue)),
				signingCredentials: creds
			);

			return new JwtSecurityTokenHandler().WriteToken(token);
		}

		public string GenerateRefreshToken()
		{
			var rndBytes = new byte[64];
			using var rng = RandomNumberGenerator.Create();
			rng.GetBytes(rndBytes);
			return Convert.ToBase64String(rndBytes);
		}
    }
}