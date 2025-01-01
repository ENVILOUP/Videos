using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace app.Models
{
    public class LoginModel
    {
        public string Username { get; set; } = null!;
		public string Password { get; set; } = null!;
    }
}