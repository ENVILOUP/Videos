using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Threading.Tasks;

namespace app.Models
{
    public class LoginModel
    {
		[Required]
        public required string Username { get; set; }

		[Required]
		public required string Password { get; set; }
    }
}