using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace app.Models
{
    public class RevokeTokenModel
    {
        public string RefreshToken { get; set; } = null!;
    }
}