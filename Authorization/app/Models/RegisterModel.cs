using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace app.Models
{
    public class RegisterModel
    {
		public string Username { get; set; } = null!;
		public string Password { get; set; } = null!;
		public string Email { get; set; } = null!;
    }
}