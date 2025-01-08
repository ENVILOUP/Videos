using app.Services;

using app.Models;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using Microsoft.OpenApi.Models;
namespace app
{
	public static class ServiceExtensions
	{
		public static void AddCustomServices(this IServiceCollection services, string connectionString)
		{
			services.AddOpenApi();
			services.AddControllers();
			services.AddScoped<JWTService>();
			services.AddDbContext<AppDbContext>(opt => opt.UseNpgsql(connectionString));
		}

		public static void ConfigureJwtAuthentication(this IServiceCollection services, IConfiguration configuration)
		{
			var key = configuration["JWT_KEY"] ?? throw new InvalidOperationException("JWT_KEY not found");

			services.AddAuthentication(opt =>
			{
				opt.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
				opt.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
			}).AddJwtBearer(opt =>
			{
				opt.TokenValidationParameters = new TokenValidationParameters
				{
					ValidateIssuer = true,
					ValidateAudience = true,
					ValidateLifetime = true,
					ValidateIssuerSigningKey = true,
					ValidIssuer = configuration["JWT:Issuer"],
					ValidAudience = configuration["JWT:Audience"],
					IssuerSigningKey = new SymmetricSecurityKey(System.Text.Encoding.UTF8.GetBytes(key))
				};
			});
		}

		public static void ConfigureSwagger(this IServiceCollection services)
		{
			services.AddSwaggerGen(opt =>
			{
				opt.SwaggerDoc("v1", new OpenApiInfo { Title = "Auth API", Version = "v1" });
				opt.AddSecurityDefinition("Bearer", new OpenApiSecurityScheme
				{
					In = ParameterLocation.Header,
					Description = "Please enter token",
					Name = "Authorization",
					Type = SecuritySchemeType.Http,
					BearerFormat = "JWT",
					Scheme = "Bearer"
				});
				opt.AddSecurityRequirement(new OpenApiSecurityRequirement
				{
				{
					new OpenApiSecurityScheme
					{
						Reference = new OpenApiReference
						{
							Type = ReferenceType.SecurityScheme,
							Id = "Bearer"
						}
					},
					Array.Empty<string>()
				}
				});
			});
		}

		public static void ConfigureIdentity(this IServiceCollection services)
		{
			services.AddIdentity<IdentityUser, IdentityRole>(opt =>
			{
				opt.Password.RequireDigit = false;
				opt.Password.RequiredLength = 3;
				opt.Password.RequireLowercase = false;
				opt.Password.RequireUppercase = false;
				opt.Password.RequireNonAlphanumeric = false;
				opt.User.RequireUniqueEmail = true;
			})
			.AddEntityFrameworkStores<AppDbContext>()
			.AddDefaultTokenProviders();
		}

		public static void ConfigureHealthChecks(this IServiceCollection services, string connectionString)
		{
			services.AddHealthChecks()
				.AddNpgSql(connectionString);
		}
	}
}