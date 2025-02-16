using app.Validators;

namespace tests;

public class MaxLengthPasswordValidatorTest
{
	private readonly MaxLengthPasswordValidator<TestUser> _validator;

	public MaxLengthPasswordValidatorTest()
	{
		_validator = new MaxLengthPasswordValidator<TestUser>(16);
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
	public async Task ValidateAsync_PasswordWithValidLength_ReturnsSuccess(string password)
	{
		var user = new TestUser();


		var result = await _validator.ValidateAsync(null!, user, password);


		Assert.True(result.Succeeded);
	}

	[Theory]
	[InlineData("test123456789012345")]
	[InlineData("abcdefg123456789012345")]
	public async Task ValidateAsync_PasswordWithInvalidLength_ReturnsFailure(string password)
	{
		var user = new TestUser();


		var result = await _validator.ValidateAsync(null!, user, password);


		Assert.False(result.Succeeded);
	}
}