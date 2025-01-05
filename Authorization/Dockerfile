FROM --platform=$BUILDPLATFORM mcr.microsoft.com/dotnet/sdk:9.0

ARG configuration=Release

ENV ASPNETCORE_URLS=http://+:8080

WORKDIR /app

COPY ./app/app.csproj /app/

RUN dotnet restore "app.csproj"

COPY ./app /app

RUN dotnet build "app.csproj" -c $configuration -o /tmp/build


EXPOSE 8080 

ENTRYPOINT ["dotnet", "/tmp/build/app.dll"]
