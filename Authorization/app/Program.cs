using app;
using app.Extensions;
using app.Models;
using Microsoft.EntityFrameworkCore;

var builder = WebApplication.CreateBuilder(args);

var connectionString = Environment.GetEnvironmentVariable("DATABASE__CONNECTIONSTRING")
					   ?? builder.Configuration.GetConnectionString("DefaultConnection");

builder.Services.AddCustomServices(connectionString!);
builder.Services.ConfigureHealthChecks(connectionString!);
builder.Services.ConfigureSwagger();
builder.Services.ConfigureIdentity();
builder.Services.ConfigureJwtAuthentication(builder.Configuration);

var app = builder.Build();

app.UseMiddleware<ExceptionMiddleware>();

app.UseDatabaseMigration();

app.UseMiddlewareComponents();

app.Run();
