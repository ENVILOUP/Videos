using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using app.Core.Models;
using FluentValidation;

namespace app.Application.Validators
{
    public class RegisterModelValidator: AbstractValidator<RegisterModel>
    {
        public RegisterModelValidator()
        {
            RuleFor(registerModel => registerModel.Username).NotEmpty().MinimumLength(4);

            RuleFor(registerModel => registerModel.Password).NotEmpty().MinimumLength(12);

            RuleFor(registerModel => registerModel.Email).NotEmpty().EmailAddress();
        }
    }
}