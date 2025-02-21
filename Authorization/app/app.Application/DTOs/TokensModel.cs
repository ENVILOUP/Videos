using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace app.Application.DTOs
{
    public class TokensModel
    {
        public required string AccessToken { get; set; }
        public required string RefreshToken { get; set; }
    }
}