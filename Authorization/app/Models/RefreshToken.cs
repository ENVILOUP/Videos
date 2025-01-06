using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Identity;

namespace app.Models
{
    public class RefreshToken
    {
		public Guid Id { get; set; }
		public required string Token { get; set; }
		public required string UserId { get; set; }
		public IdentityUser? User { get; set; }
		public DateTime ExpiryDate { get; set; }
		public bool IsRevoked { get; set; }
		public bool IsUsed { get; set; }
    }
}