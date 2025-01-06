using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Threading.Tasks;

namespace app.Models
{
    public class RegisterModel
    {
		[Required]
		public required string Username { get; set; }

		[Required]
		public required string Password { get; set; }

		[Required]
		[EmailAddress]
		public required string Email { get; set; }
    }
}