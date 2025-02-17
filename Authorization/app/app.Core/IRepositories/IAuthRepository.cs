using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using app.Core.Models;
using Microsoft.AspNetCore.Identity;
using Microsoft.AspNetCore.Mvc;

namespace app.Core.IRepositories
{
	public interface IAuthRepository
	{
		Task<IdentityResult> AddNewUser(IdentityUser user, string password);
		Task AddRefreshToken(RefreshToken refreshTokenEntity);
		Task UpdateRefreshToken(RefreshToken newRefreshTokenEntity, RefreshToken oldRefreshTokenEntity);
		Task RevokeRefreshToken(RefreshToken refreshToken);
		Task UserLogout(List<RefreshToken> tokens);
    }
}