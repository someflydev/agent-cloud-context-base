FROM mcr.microsoft.com/dotnet/sdk:8.0@sha256:4b1cdaa57eed2cecabcf29bdb9bce11e8ca1c287d39dfd2c8b534663ea94d493 AS build
WORKDIR /src
COPY src/Accb.ContainerApps.Dapr/Accb.ContainerApps.Dapr.csproj ./Accb.ContainerApps.Dapr/
RUN dotnet restore ./Accb.ContainerApps.Dapr/Accb.ContainerApps.Dapr.csproj
COPY src/Accb.ContainerApps.Dapr ./Accb.ContainerApps.Dapr
RUN dotnet publish ./Accb.ContainerApps.Dapr/Accb.ContainerApps.Dapr.csproj -c Release -o /out

FROM mcr.microsoft.com/dotnet/aspnet:8.0@sha256:f88c77644f4c480a62d3b46dc74db8d5472a24e282df8b1e56195c689d35a6db AS runtime
ENV ASPNETCORE_URLS=http://0.0.0.0:8080 \
    PORT=8080
WORKDIR /app
COPY --from=build /out .
USER $APP_UID
EXPOSE 8080
HEALTHCHECK CMD ["dotnet", "Accb.ContainerApps.Dapr.dll", "--healthcheck"]
ENTRYPOINT ["dotnet", "Accb.ContainerApps.Dapr.dll"]
