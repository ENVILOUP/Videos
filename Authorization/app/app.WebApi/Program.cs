using app.WebApi.Extensions;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

var connectionString = Environment.GetEnvironmentVariable("DATABASE__CONNECTIONSTRING")
					   ?? builder.Configuration.GetConnectionString("DefaultConnection");

if (string.IsNullOrEmpty(connectionString))
{
	throw new InvalidOperationException("Connection string not found");
}

builder.Services.AddCustomServices(connectionString);
builder.Services.AddValidators();
builder.Services.ConfigureHealthChecks(connectionString);
builder.Services.ConfigureSwagger();
builder.Services.ConfigureIdentity();
builder.Services.ConfigureJwtAuthentication(builder.Configuration);

var app = builder.Build();

app.UseMiddleware<ExceptionMiddleware>();

app.UseDatabaseMigration();

app.UseMiddlewareComponents();

app.Run();
