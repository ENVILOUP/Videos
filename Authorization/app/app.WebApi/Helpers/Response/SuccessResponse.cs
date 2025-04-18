using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json.Serialization;
using System.Threading.Tasks;
using app.Core.Models;

namespace app.WebApi.Helpers.Response
{
    public class SuccessResponse<T>
    {
        [JsonPropertyName("success")]
		public bool Success { get; set; } = true;

		[JsonPropertyName("data")]
		public required T Data { get; set; }

		[JsonPropertyName("status_code")]
		public AuthResponseStatusCode StatusCode { get; set; }
    }
}