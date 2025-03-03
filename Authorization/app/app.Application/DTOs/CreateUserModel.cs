using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace app.Application.DTOs
{
    public class CreateUserModel
    {
        public required string Username { get; set; }
        public required string Password { get; set; }
        public required string Email { get; set; }
        public required string Role { get; set; }
    }
}