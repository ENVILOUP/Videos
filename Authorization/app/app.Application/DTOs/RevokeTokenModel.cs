using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Threading.Tasks;

namespace app.Application.DTOs
{
    public class RevokeTokenModel
    {
        public required string RefreshToken { get; set; }
    }
}