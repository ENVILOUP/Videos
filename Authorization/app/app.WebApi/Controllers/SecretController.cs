using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using app.WebApi.Helpers.Response;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace app.WebApi.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class SecretController : ControllerBase
    {
        [HttpGet]
		[Authorize]
		public IActionResult GetSecretData() => ResponseHelper.Ok("Secret data");
    }
}