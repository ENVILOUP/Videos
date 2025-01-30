using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using app.Models;
using FluentValidation;

namespace app.Validators
{
    public class RegisterModelValidator: AbstractValidator<RegisterModel>
    {
        public RegisterModelValidator()
        {
            RuleFor(registerModel => registerModel.Username).NotEmpty().MinimumLength(2);

            RuleFor(registerModel => registerModel.Password).NotEmpty().MinimumLength(3);

            RuleFor(registerModel => registerModel.Email).NotEmpty().EmailAddress();
        }
    }
}