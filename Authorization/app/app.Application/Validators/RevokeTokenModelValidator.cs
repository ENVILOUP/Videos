using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using app.Core.Models;
using FluentValidation;

namespace app.Application.Validators
{
	public class RevokeTokenModelValidator : AbstractValidator<RevokeTokenModel>
	{
		public RevokeTokenModelValidator()
		{
			RuleFor(revokeTokenModel => revokeTokenModel.RefreshToken).NotEmpty();
		}
    }
}