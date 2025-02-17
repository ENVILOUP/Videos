using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Identity;

namespace app.Validators
{
	public class ValidSymbolsPasswordValidator<TUser> : IPasswordValidator<TUser> where TUser : class
	{
		private readonly HashSet<char> _validSymbols = [.. "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*+-_(){}[]'\":;.,/?`~\\|"];

		public Task<IdentityResult> ValidateAsync(UserManager<TUser> manager, TUser user, string? password)
		{
			if (password is null) return Task.FromResult(IdentityResult.Success);

			if (password.Any(symbol => !_validSymbols.Contains(symbol)))
			{
				return Task.FromResult(IdentityResult.Failed(new IdentityError
				{
					Code = "InvalidSymbols",
					Description = "Password contains invalid symbols."
				}));
			}

			return Task.FromResult(IdentityResult.Success);
		}
	}
}