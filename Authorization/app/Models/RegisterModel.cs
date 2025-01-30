using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Threading.Tasks;

namespace app.Models
{
    public class RegisterModel
    {
		public required string Username { get; set; }
		public required string Password { get; set; }
		public required string Email { get; set; }
    }
}