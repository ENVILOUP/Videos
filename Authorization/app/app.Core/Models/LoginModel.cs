using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Threading.Tasks;

namespace app.Core.Models
{
    public class LoginModel
    {
        public required string Username { get; set; }
		public required string Password { get; set; }
    }
}