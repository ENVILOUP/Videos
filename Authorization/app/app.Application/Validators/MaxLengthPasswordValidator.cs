using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Identity;

namespace app.Application.Validators
{
	public class MaxLengthPasswordValidator<TUser> : IPasswordValidator<TUser> where TUser : class
	{
		private readonly int _maxPasswordLength = 64;

		public Task<IdentityResult> ValidateAsync(UserManager<TUser> manager, TUser user, string? password)
		{
			if (password is null) return Task.FromResult(IdentityResult.Success);

			if (password.Length > _maxPasswordLength)
			{
				return Task.FromResult(IdentityResult.Failed(new IdentityError
				{
					Code = "PasswordTooLong",
					Description = $"Password cannot be longer than {_maxPasswordLength} characters."
				}));
			}

			return Task.FromResult(IdentityResult.Success);
		}
	}
}