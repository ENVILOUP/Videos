namespace app.Models.Response
{
	public enum AuthResponseStatusCode
	{
		// ✅ Успешные операции
		Ok = 2000,
		Registered = 2100,        // Пользователь успешно зарегистрирован
		LoggedIn = 2101,          // Успешный вход в систему
		TokenRefreshed = 2102,    // Токен успешно обновлён
		TokenRevoked = 2103,      // Токен успешно отозван
		LoggedOut = 2104,         // Успешный выход из системы

		// ⚠️ Ошибки валидации
		RegisterNotValidData = 4000,    // Ошибка валидации данных регистрации
		LoginNotValidData = 4001,       // Ошибка валидации данных входа
		RefreshTokenNotValidData = 4002,// Ошибка валидации данных обновления токена
		RevokeTokenNotValidData = 4003, // Ошибка валидации данных отзыва токена

		// ❌ Ошибки аутентификации и авторизации
		RegistrationFailed = 4100,  // Ошибка регистрации
		UserNotFound = 4101,        // Пользователь не найден
		LoginNotMatchPassword = 4102, // Неверный пароль
		RefreshTokenNotFound = 4103, // Токен не найден
		InvalidToken = 4104,        // Недействительный токен
		TokenExpired = 4105,        // Истёк срок действия токена
		TokenRevokeFailed = 4106,   // Ошибка отзыва токена
		TokenAlreadyRevoked = 4107, // Токен уже отозван

		// 🔥 Внутренние ошибки сервера
		ServerError = 5000          // Внутренняя ошибка сервера
	}
}