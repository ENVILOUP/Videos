using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using app.Application.DTOs;
using FluentValidation;

namespace app.Application.Validators
{
	public class RefreshTokenModelValidator : AbstractValidator<RefreshTokenModel>
	{
		public RefreshTokenModelValidator()
		{
			RuleFor(refreshTokenModel => refreshTokenModel.RefreshToken).NotEmpty();
		}
    }
}