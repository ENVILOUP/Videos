using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using app.Core.Models.Response;

namespace app.Core.Models
{
	public class ServiceResult<T>
	{
		public bool Success { get; set; }
		public T? Data { get; set; }
		public AuthResponseStatusCode StatusCode { get; set; }

		public static ServiceResult<T> Ok(T data, AuthResponseStatusCode statusCode = AuthResponseStatusCode.Ok) =>
			new() { Success = true, Data = data, StatusCode = statusCode };

		public static ServiceResult<T> Fail(AuthResponseStatusCode statusCode) =>
			new() { Success = false, StatusCode = statusCode };
	}

}