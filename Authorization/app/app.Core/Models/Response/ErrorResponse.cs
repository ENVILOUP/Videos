using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

namespace app.Core.Models.Response
{
    public class ErrorResponse
    {
        [JsonPropertyName("success")]
		public bool Success { get; set; } = false;

		[JsonPropertyName("status_code")]
		public AuthResponseStatusCode StatusCode { get; set; }
    }
}