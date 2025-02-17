using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using Microsoft.IdentityModel.Tokens;
using Microsoft.OpenApi.Models;
using FluentValidation;
using app.Application.Validators;
using app.Infrastructure;
using app.Application.Services;
using app.Core.IRepositories;
using app.Infrastructure.Repositories;
using app.Core.Models;

namespace app.WebApi.Extensions
{
	public static class ServiceExtensions
	{
		public static void AddCustomServices(this IServiceCollection services, string connectionString)
		{
			services.AddOpenApi();
			services.AddControllers();

			// services
			services.AddScoped<JWTService>();
			services.AddScoped<AuthService>();

			// repositories
			services.AddScoped<IAuthRepository, AuthRepository>();

			services.AddDbContext<AppDbContext>(opt => opt.UseNpgsql(connectionString));
			services.AddDefaultCors();
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
				opt.MapInboundClaims = false;
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
				opt.Password.RequiredLength = 12;
				opt.Password.RequireDigit = true;
				opt.Password.RequireLowercase = true;
				opt.Password.RequireUppercase = false;
				opt.Password.RequireNonAlphanumeric = false;
				opt.User.RequireUniqueEmail = true;
			})
			.AddEntityFrameworkStores<AppDbContext>()
			.AddDefaultTokenProviders();

			services.AddScoped<IPasswordValidator<IdentityUser>>(provider =>
			 new MaxLengthPasswordValidator<IdentityUser>());

			services.AddScoped<IPasswordValidator<IdentityUser>>(provider =>
			 new ValidSymbolsPasswordValidator<IdentityUser>());
		}

		public static void ConfigureHealthChecks(this IServiceCollection services, string connectionString)
		{
			services.AddHealthChecks()
				.AddNpgSql(connectionString);
		}

		public static void AddValidators(this IServiceCollection services)
		{
			services.AddScoped<IValidator<RegisterModel>, RegisterModelValidator>();
			services.AddScoped<IValidator<LoginModel>, LoginModelValidator>();
			services.AddScoped<IValidator<RefreshTokenModel>, RefreshTokenModelValidator>();
			services.AddScoped<IValidator<RevokeTokenModel>, RevokeTokenModelValidator>();
		}

		public static void AddDefaultCors(this IServiceCollection services)
		{
			services.AddCors(opt =>
			{
				opt.AddDefaultPolicy(builder =>
				{
					builder.AllowAnyOrigin();
					builder.AllowAnyMethod();
					builder.AllowAnyHeader();
				});
			});
		}
	}
}