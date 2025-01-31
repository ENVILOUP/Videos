using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;

namespace app.Models.Response
{
	public static class ResponseHelper
	{
		public static IActionResult Ok<T>(T data, AuthResponseStatusCode statusCode = AuthResponseStatusCode.Ok)
		{
			var response = new SuccessResponse<T>
			{
				StatusCode = statusCode,
				Data = data
			};
			return new OkObjectResult(response);
		}

		public static IActionResult Error(AuthResponseStatusCode statusCode)
		{
			var response = new ErrorResponse
			{
				Success = false,
				StatusCode = statusCode
			};
			return new BadRequestObjectResult(response);
		}
	}
}