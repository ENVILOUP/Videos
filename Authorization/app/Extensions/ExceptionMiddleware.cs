using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace app.Extensions
{
	public class ExceptionMiddleware
	{
		private readonly RequestDelegate _next;
		private readonly ILogger<ExceptionMiddleware> _logger;

		public ExceptionMiddleware(RequestDelegate next, ILogger<ExceptionMiddleware> logger)
		{
			_next = next;
			_logger = logger;
		}

		public async Task InvokeAsync(HttpContext context)
		{
			try
			{
				await _next(context);
			}
			catch (Exception ex)
			{
				_logger.LogError($"Ошибка: {ex.Message}");
				await HandleExceptionAsync(context, ex);
			}
		}

		private static Task HandleExceptionAsync(HttpContext context, Exception exception)
		{
			context.Response.ContentType = "application/json";
			context.Response.StatusCode = StatusCodes.Status500InternalServerError;

			var response = new
			{
				StatusCode = context.Response.StatusCode,
				Message = "Server error.",
				// DetailedMessage = exception.Message // Уберите, если не хотите показывать детали.
			};

			return context.Response.WriteAsJsonAsync(response);
		}
	}

}