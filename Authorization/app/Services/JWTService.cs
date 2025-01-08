using System;
using System.Collections.Generic;
using System.IdentityModel.Tokens.Jwt;
using System.Linq;
using System.Security.Claims;
using System.Security.Cryptography;
using System.Text;
using System.Threading.Tasks;
using app.Models;
using Microsoft.AspNetCore.Identity;
using Microsoft.IdentityModel.Tokens;

namespace app.Services
{
    public class JWTService(IConfiguration configuration, ILogger<JWTService> logger)
    {
		private readonly IConfiguration _configuration = configuration;
		private readonly ILogger<JWTService> _logger = logger;

        public string GenerateJwtToken(IdentityUser user)
		{
			var jtiId = Guid.NewGuid().ToString();
			var claims = new[]
			{
				new Claim(ClaimTypes.NameIdentifier, user.Id),
				new Claim(JwtRegisteredClaimNames.Sub, user.Id),
				new Claim(JwtRegisteredClaimNames.Jti, jtiId),
				new Claim(ClaimTypes.Name, user.UserName ?? throw new InvalidOperationException("Username not found")),
			};

			string jwtKey = _configuration["JWT_KEY"] ?? throw new InvalidOperationException("JWT_Key not found");

			if (string.IsNullOrEmpty(jwtKey))
			{
				throw new InvalidOperationException("JWT_Key not found");
			}

			_logger.LogInformation($"JWT_KEY: {jwtKey}");

			var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(jwtKey));

			var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

			var expiresValue = _configuration.GetSection("JWT:AccessTokenExpirationMinutes").Value;

			if (string.IsNullOrEmpty(expiresValue))
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