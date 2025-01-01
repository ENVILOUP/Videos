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
    public class JWTService(IConfiguration configuration)
    {
		private readonly IConfiguration _configuration = configuration;
        public string GenerateJwtToken(IdentityUser user)
		{
			var jtiId = Guid.NewGuid().ToString();
			var claims = new[]
			{
				new Claim(ClaimTypes.NameIdentifier, user.Id),
				new Claim(JwtRegisteredClaimNames.Sub, user.Id),
				new Claim(JwtRegisteredClaimNames.Jti, jtiId),
				new Claim(ClaimTypes.Name, user.UserName!)
			};

			var key = new SymmetricSecurityKey(Encoding.UTF8.GetBytes(_configuration["JWT:Key"]!));

			var creds = new SigningCredentials(key, SecurityAlgorithms.HmacSha256);

			var token = new JwtSecurityToken(
				issuer: _configuration["JWT:Issuer"],
				audience: _configuration["JWT:Audience"],
				claims: claims,
				expires: DateTime.UtcNow.AddMinutes(_configuration.GetValue<int>("JWT:AccessTokenExpiration")),
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