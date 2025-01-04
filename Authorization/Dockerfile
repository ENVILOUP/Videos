FROM --platform=$BUILDPLATFORM mcr.microsoft.com/dotnet/sdk:9.0

ARG configuration=Debug

ENV ASPNETCORE_URLS=http://+:5025

WORKDIR /app

COPY ./app/app.csproj /app/

RUN dotnet restore "app.csproj"

COPY ./app /app

RUN dotnet build "app.csproj" -c $configuration -o /tmp/build

USER app

EXPOSE 5025

ENTRYPOINT ["dotnet", "/tmp/build/app.dll"]
