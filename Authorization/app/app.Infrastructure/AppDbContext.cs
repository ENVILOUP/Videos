using Microsoft.EntityFrameworkCore;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.AspNetCore.Identity;
using app.Core.Models;

namespace app.Infrastructure
{
	public class AppDbContext : IdentityDbContext<IdentityUser>
	{
		public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }

		public DbSet<RefreshToken> RefreshTokens { get; set; }

		protected override void OnModelCreating(ModelBuilder builder)
		{
			base.OnModelCreating(builder);
			builder.Entity<RefreshToken>()
				.HasOne(refreshToken => refreshToken.User)
				.WithMany()
				.HasForeignKey(refreshToken => refreshToken.UserId);
		}
	}
}