using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using app.Application.IRepositories;
using Microsoft.AspNetCore.Identity;

namespace app.Infrastructure.Repositories
{
    public class UserRepository : IUserRepository
    {
        private readonly UserManager<IdentityUser> _userManager;

        public UserRepository(UserManager<IdentityUser> userManager)
        {
            _userManager = userManager;
        }

        public async Task<IdentityResult> AddNewUser(IdentityUser user, string password)
        {
            var result = await _userManager.CreateAsync(user, password);

            return result;
        }
    }
}