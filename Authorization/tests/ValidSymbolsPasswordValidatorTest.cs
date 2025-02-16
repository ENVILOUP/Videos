using app.Validators;
using Microsoft.AspNetCore.Identity;
namespace tests;

public class TestUser {}

public class ValidSymbolsPasswordValidatorTest
{
	private readonly HashSet<char> _validSymbols = [.. "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*+-_(){}[]'\":;.,/?`~\\|"];

	private readonly ValidSymbolsPasswordValidator<TestUser> _validator;

	public ValidSymbolsPasswordValidatorTest()
	{
		_validator = new ValidSymbolsPasswordValidator<TestUser>(_validSymbols);
	}

	[Fact]
	public async Task ValidateAsync_NullPassword_ReturnsSuccess()
	{
		var user = new TestUser();
		string? password = null;


		var result = await _validator.ValidateAsync(null!, user, password);


		Assert.True(result.Succeeded);
	}

	[Theory]
	[InlineData("test1234")]
	[InlineData("abcdefg1234")]
	[InlineData("1234567890")]
	[InlineData("AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz")]
	public async Task ValidateAsync_PasswordWithValidSymbols_ReturnsSuccess(string password)
	{
		var user = new TestUser();


		var result = await _validator.ValidateAsync(null!, user, password);


		Assert.True(result.Succeeded);
	}

	[Theory]
	[InlineData("test1234ℵ")]
	[InlineData("abcde✿fg1234")]
	[InlineData("☀1234567890")]
	[InlineData("ټAaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz")]
	public async Task ValidateAsync_PasswordWithInvalidSymbols_ReturnsFailure(string password)
	{
		var user = new TestUser();


		var result = await _validator.ValidateAsync(null!, user, password);


		Assert.False(result.Succeeded);
	}
}
