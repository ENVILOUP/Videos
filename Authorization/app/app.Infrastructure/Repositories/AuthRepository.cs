using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using app.Core.IRepositories;
using app.Core.Models;
using app.Core.Models.Response;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;

namespace app.Infrastructure.Repositories
{
	public class AuthRepository : IAuthRepository
	{
		private readonly UserManager<IdentityUser> _userManager;
		private readonly AppDbContext _dbContext;

		public AuthRepository(UserManager<IdentityUser> userManager, AppDbContext dbContext)
		{
			_userManager = userManager;
			_dbContext = dbContext;
		}

		public async Task<IdentityResult> AddNewUser(IdentityUser user, string password)
		{
			try
			{
				var result = await _userManager.CreateAsync(user, password);

				return result;
			}
			catch (Exception)
			{
				throw;
			}
		}

		public async Task AddRefreshToken(RefreshToken refreshTokenEntity)
		{
			try
			{
				await _dbContext.RefreshTokens.AddAsync(refreshTokenEntity);
				await _dbContext.SaveChangesAsync();
			}
			catch (Exception)
			{
				throw;
			}
		}

		public async Task RevokeRefreshToken(RefreshToken refreshToken)
		{
			try
			{
				refreshToken.IsRevoked = true;

				_dbContext.RefreshTokens.Update(refreshToken);
				await _dbContext.SaveChangesAsync();
			}
			catch (Exception)
			{
				throw;
			}
		}

		public async Task UpdateRefreshToken(RefreshToken newRefreshTokenEntity, RefreshToken oldRefreshTokenEntity)
		{
			using var transaction = _dbContext.Database.BeginTransaction();

			await _dbContext.RefreshTokens.AddAsync(newRefreshTokenEntity);

			oldRefreshTokenEntity.IsUsed = true;
			_dbContext.RefreshTokens.Update(oldRefreshTokenEntity);
			await _dbContext.SaveChangesAsync();

			await transaction.CommitAsync();
		}

		public async Task UserLogout(List<RefreshToken> tokens)
		{
			try
			{
				tokens.ForEach(refreshToken => refreshToken.IsRevoked = true);
				_dbContext.RefreshTokens.UpdateRange(tokens);

				await _dbContext.SaveChangesAsync();
			}
			catch (Exception)
			{
				throw;
			}
		}
	}
}