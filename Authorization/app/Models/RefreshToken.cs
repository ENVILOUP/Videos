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
		public string Token { get; set; } = null!;
		public string UserId { get; set; } = null!;
		public IdentityUser User { get; set; } = null!;
		public DateTime ExpiryDate { get; set; }
		public bool IsRevoked { get; set; }
		public bool IsUsed { get; set; }
    }
}