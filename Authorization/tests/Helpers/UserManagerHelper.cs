using Microsoft.AspNetCore.Identity;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using Moq;

namespace tests.Helpers;

public class UserManagerHelper
{
	public static UserManager<IdentityUser> CreateDefaultUserManager()
	{
		var storeMock = new Mock<IUserStore<IdentityUser>>();
		var optionsMock = new Mock<IOptions<IdentityOptions>>();
		optionsMock.Setup(o => o.Value).Returns(new IdentityOptions());
		var userValidators = new List<IUserValidator<IdentityUser>>();
		var passwordValidators = new List<IPasswordValidator<IdentityUser>>();
		var passwordHasher = new PasswordHasher<IdentityUser>();
		var lookupNormalizer = new UpperInvariantLookupNormalizer();
		var errors = new IdentityErrorDescriber();
		var services = new ServiceCollection().BuildServiceProvider();
		var loggerMock = new Mock<ILogger<UserManager<IdentityUser>>>();

		return new UserManager<IdentityUser>(
			storeMock.Object,
			optionsMock.Object,
			passwordHasher,
			userValidators,
			passwordValidators,
			lookupNormalizer,
			errors,
			services,
			loggerMock.Object);
	}
}