FROM --platform=$BUILDPLATFORM mcr.microsoft.com/dotnet/sdk:9.0

ARG configuration=Release

ENV ASPNETCORE_URLS=http://+:8080

WORKDIR /app

COPY ./app/app.sln ./
COPY ./app/app.Application/*.csproj ./app.Application/
COPY ./app/app.Core/*.csproj ./app.Core/
COPY ./app/app.Infrastructure/*.csproj ./app.Infrastructure/
COPY ./app/app.WebApi/*.csproj ./app.WebApi/

RUN dotnet restore "app.WebApi/app.WebApi.csproj"

COPY ./app ./

RUN dotnet build "app.WebApi/app.WebApi.csproj" -c $configuration -o /tmp/build

EXPOSE 8080 

ENTRYPOINT ["dotnet", "/tmp/build/app.WebApi.dll"]