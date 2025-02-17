using app.Infrastructure;
using app.Core.Models;
using Microsoft.AspNetCore.Diagnostics.HealthChecks;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.Diagnostics.HealthChecks;
using Microsoft.OpenApi.Models;

namespace app.WebApi.Extensions
{
	public static class MiddlewareExtensions
	{
		public static void UseSwaggerDocumentation(this IApplicationBuilder app)
		{
			app.UseSwagger(c =>
			{
				c.PreSerializeFilters.Add((swagger, httpReq) =>
				{
					swagger.Servers = new List<OpenApiServer>
					{
					new OpenApiServer { Url = $"{httpReq.Scheme}://{httpReq.Host.Value}/{httpReq.Headers["X-Forwarded-Prefix"]}" }
					};
				});
			});

			app.UseSwaggerUI(c =>
			{
				c.SwaggerEndpoint("/swagger/v1/swagger.json", "Auth API v1");
				c.RoutePrefix = "docs";
			});
		}

		public static void MapCustomHealthChecks(this IEndpointRouteBuilder endpoints)
		{
			endpoints.MapHealthChecks("/health-check", new HealthCheckOptions
			{
				ResponseWriter = async (context, report) =>
				{
					context.Response.ContentType = "application/json";

					if (report.Status == HealthStatus.Healthy)
					{
						context.Response.StatusCode = StatusCodes.Status200OK;
						var successResult = new
						{
							status = 200,
							message = "OK"
						};
						await context.Response.WriteAsJsonAsync(successResult);
						return;
					}

					context.Response.StatusCode = StatusCodes.Status500InternalServerError;

					var failedCheck = report.Entries
						.FirstOrDefault(entry => entry.Value.Status != HealthStatus.Healthy);

					var errorMessage = failedCheck.Key != null
						? $"{failedCheck.Key}"
						: "Unknown error";

					var errorResult = new
					{
						status = 500,
						message = errorMessage
					};

					await context.Response.WriteAsJsonAsync(errorResult);
				}
			});
		}

		public static void UseDatabaseMigration(this IApplicationBuilder app)
		{
			using var scope = app.ApplicationServices.CreateScope();
			var dbContext = scope.ServiceProvider.GetRequiredService<AppDbContext>();

			try
			{
				dbContext.Database.Migrate();
			}
			catch (Exception ex)
			{
				Console.WriteLine($"Error applying migrations: {ex.Message}");
				throw;
			}
		}

		public static void UseMiddlewareComponents(this IApplicationBuilder app)
		{
			app.UseSwaggerDocumentation(); // Swagger для документации
			app.UseRouting(); // Настраиваем маршрутизацию
			app.UseAuthentication(); // Аутентификация
			app.UseAuthorization();  // Авторизация
			app.UseCors(); // CORS
			app.UseEndpoints(endpoints =>
			{
				endpoints.MapGet("/", () => "pong");
				endpoints.MapControllers(); // Подключаем контроллеры
				endpoints.MapCustomHealthChecks(); // Подключаем проверки состояния
			});
		}
	}
}
