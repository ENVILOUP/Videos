namespace app.Core.Models
{
	public enum AuthResponseStatusCode
	{
		// ✅ Successful operations 
		Ok = 2000,
		Registered = 2100,
		LoggedIn = 2101,
		TokenRefreshed = 2102, 
		TokenRevoked = 2103,
		LoggedOut = 2104,
		UserCreated = 2105,

		// ⚠️ Validation errors
		RegisterNotValidData = 4000,
		LoginNotValidData = 4001,
		RefreshTokenNotValidData = 4002,
		RevokeTokenNotValidData = 4003,

		// ❌ Authentication and authorization errors
		RegistrationFailed = 4100,
		UserNotFound = 4101,
		LoginNotMatchPassword = 4102,
		RefreshTokenNotFound = 4103,
		InvalidToken = 4104,
		TokenExpired = 4105,
		TokenRevokeFailed = 4106,
		TokenAlreadyRevoked = 4107,
		SQLException = 4108,
		CreateUserNotValidData = 4109,
		RoleNotSupported = 4110,

		// 🔥 Server errors
		ServerError = 5000 
	}
}
