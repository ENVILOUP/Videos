using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using app.Core.Models;

namespace app.Application.IRepositories
{
    public interface IRefreshTokenRepository
    {
		Task AddRefreshToken(RefreshToken refreshTokenEntity);
		Task UpdateRefreshToken(RefreshToken newRefreshTokenEntity, RefreshToken oldRefreshTokenEntity);
		Task RevokeRefreshToken(RefreshToken refreshToken);
		Task RevokeRefreshTokens(List<RefreshToken> tokens);
		Task<RefreshToken?> FindRefreshTokenByTokenId(string tokenId);
		Task<List<RefreshToken>> FindRefreshTokensByUserId(string userId);
    }
}