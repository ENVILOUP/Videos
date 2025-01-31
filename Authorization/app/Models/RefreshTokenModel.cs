using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Threading.Tasks;

namespace app.Models
{
    public class RefreshTokenModel
    {
        public required string RefreshToken { get; set; }
    }
}