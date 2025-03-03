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
        private readonly RoleManager<IdentityRole> _roleManager;

        public UserRepository(UserManager<IdentityUser> userManager, RoleManager<IdentityRole> roleManager)
        {
            _userManager = userManager;
            _roleManager = roleManager;
        }

        public async Task<IdentityResult> AddNewUser(IdentityUser user, string password)
        {
            var result = await _userManager.CreateAsync(user, password);

            return result;
        }

        public async Task<IdentityResult> ApplyUserRole(IdentityUser user)
        {
            var role = await _roleManager.FindByNameAsync("User") ?? throw new Exception("Role not found");

            var result = await _userManager.AddToRoleAsync(user, role.Name ?? throw new Exception("Role name not initialized"));

            return result;
        }

        public async Task<IdentityResult> ApplyUserRole(IdentityUser user, string role)
        {
            var roleEntity = await _roleManager.FindByNameAsync(role) ?? throw new Exception("Role not found");

            var result = await _userManager.AddToRoleAsync(user, roleEntity.Name ?? throw new Exception("Role name not initialized"));

            return result;
        }

        public async Task<string> GetUserRole(IdentityUser user)
        {
            var role = await _userManager.GetRolesAsync(user);

            return role.FirstOrDefault() ?? throw new Exception("Role not found");
        }
    }
}