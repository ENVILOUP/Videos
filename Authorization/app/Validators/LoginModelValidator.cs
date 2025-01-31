using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using app.Models;
using FluentValidation;

namespace app.Validators
{
	public class LoginModelValidator : AbstractValidator<LoginModel>
	{
		public LoginModelValidator()
		{
			RuleFor(loginModel => loginModel.Username).NotEmpty().MinimumLength(4);

			RuleFor(loginModel => loginModel.Password).NotEmpty().MinimumLength(12);
		}
    }
}