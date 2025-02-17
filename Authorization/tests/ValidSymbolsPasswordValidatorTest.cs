using app.Application.Validators;
using Microsoft.AspNetCore.Identity;
using Moq;
using tests.Helpers;
namespace tests;

public class ValidSymbolsPasswordValidatorTest
{
	private readonly ValidSymbolsPasswordValidator<IdentityUser> _validator;
	private readonly IdentityUser _user;
	private readonly UserManager<IdentityUser> _userManager;

	public ValidSymbolsPasswordValidatorTest()
	{
		_validator = new ValidSymbolsPasswordValidator<IdentityUser>();
		_user = new IdentityUser();
		_userManager = UserManagerHelper.CreateDefaultUserManager();
	}

	[Fact]
	public async Task ValidateAsync_NullPassword_ReturnsSuccess()
	{
		string? password = null;


		var result = await _validator.ValidateAsync(_userManager, _user, password);


		Assert.True(result.Succeeded);
	}

	[Theory]
	[InlineData("test1234")]
	[InlineData("abcdefg1234")]
	[InlineData("1234567890")]
	[InlineData("AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz")]
	public async Task ValidateAsync_PasswordWithValidSymbols_ReturnsSuccess(string password)
	{
		var result = await _validator.ValidateAsync(_userManager, _user, password);


		Assert.True(result.Succeeded);
	}

	[Theory]
	[InlineData("test1234ℵ")]
	[InlineData("abcde✿fg1234")]
	[InlineData("☀1234567890")]
	[InlineData("ټAaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz")]
	public async Task ValidateAsync_PasswordWithInvalidSymbols_ReturnsFailure(string password)
	{
		var result = await _validator.ValidateAsync(_userManager, _user, password);


		Assert.False(result.Succeeded);
	}
}
