using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using app.Application.IRepositories;
using app.Core.Models;
using Microsoft.EntityFrameworkCore;

namespace app.Infrastructure.Repositories
{
    public class RefreshTokenRepository : IRefreshTokenRepository
    {
        private readonly AppDbContext _dbContext;

        public RefreshTokenRepository(AppDbContext dbContext)
        {
            _dbContext = dbContext;
        }

        public async Task AddRefreshToken(RefreshToken refreshTokenEntity)
		{
			await _dbContext.RefreshTokens.AddAsync(refreshTokenEntity);
			await _dbContext.SaveChangesAsync();
		}

		public async Task<RefreshToken?> FindRefreshTokenByTokenId(string tokenId)
		{
			var refreshToken = await _dbContext.RefreshTokens.FirstOrDefaultAsync(refreshToken => refreshToken.Token == tokenId);

			return refreshToken ?? null;
		}

		public async Task<List<RefreshToken>> FindRefreshTokensByUserId(string userId)
		{
			var refreshTokens = await _dbContext.RefreshTokens.Where(refreshToken => refreshToken.UserId == userId).ToListAsync();

			return refreshTokens;
		}

        public async Task RevokeRefreshToken(RefreshToken refreshToken)
		{
			refreshToken.IsRevoked = true;

			_dbContext.RefreshTokens.Update(refreshToken);
			await _dbContext.SaveChangesAsync();
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

		public async Task RevokeRefreshTokens(List<RefreshToken> tokens)
		{
			tokens.ForEach(refreshToken => refreshToken.IsRevoked = true);
			_dbContext.RefreshTokens.UpdateRange(tokens);

			await _dbContext.SaveChangesAsync();
		}
    }
}