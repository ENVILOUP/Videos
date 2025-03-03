using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Identity;

namespace app.Application.IRepositories
{
    public interface IUserRepository
    {
        Task<IdentityResult> AddNewUser(IdentityUser user, string password);
        Task<IdentityResult> ApplyUserRole(IdentityUser user);
        Task<IdentityResult> ApplyUserRole(IdentityUser user, string role);
        Task<string> GetUserRole(IdentityUser user);
    }
}