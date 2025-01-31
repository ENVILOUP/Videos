using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using app.Models;
using FluentValidation;

namespace app.Validators
{
	public class RefreshTokenModelValidator : AbstractValidator<RefreshTokenModel>
	{
		public RefreshTokenModelValidator()
		{
			RuleFor(refreshTokenModel => refreshTokenModel.RefreshToken).NotEmpty();
		}
    }
}