using app.Validators;
using Microsoft.AspNetCore.Identity;
using tests.Helpers;

namespace tests;

public class MaxLengthPasswordValidatorTest
{
	private readonly MaxLengthPasswordValidator<IdentityUser> _validator;
	private readonly UserManager<IdentityUser> _userManager;
	private readonly IdentityUser _user;

	public MaxLengthPasswordValidatorTest()
	{
		_validator = new MaxLengthPasswordValidator<IdentityUser>();
		_userManager = UserManagerHelper.CreateDefaultUserManager();
		_user = new IdentityUser();
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
	public async Task ValidateAsync_PasswordWithValidLength_ReturnsSuccess(string password)
	{
		var result = await _validator.ValidateAsync(_userManager, _user, password);


		Assert.True(result.Succeeded);
	}

	[Theory]
	[InlineData("gV7!hD@x9pR25BmNqFzXJ8dCMV$ZoPkA&EfWuTysKwL6#tY5BmNqFzXJ8dCMV$ZoPkA&EfWuTys3*")]
	[InlineData("abcdetJqV7X9hNpY5DfgtJqV712345X9hNpY5D12345678901tJqV7X9hNpY5D2345")]
	public async Task ValidateAsync_PasswordWithInvalidLength_ReturnsFailure(string password)
	{
		var result = await _validator.ValidateAsync(_userManager, _user, password);


		Assert.False(result.Succeeded);
	}
}