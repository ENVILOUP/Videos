# Authorization Service

This service is responsible for handling user authentication and authorization.

[Swagger](http://auth.api.enviloup.localhost/docs)

## Development

Before starting development, ensure that you have the following installed:

1. Docker
2. Docker Compose

### Steps to get started

1. **Build the Docker containers**

   To build the necessary Docker images, run:

   ```shell
   docker-compose build
   ```

2. **Run the service in development mode**

   To start the service and related containers (e.g., the database), run:

   ```shell
   docker-compose up -d
   ```

   This will start the services in the background. If you want to view the logs of the containers, you can run:

   ```shell
   docker-compose logs -f
   ```
3. **Access the Swagger UI**

   The service provides a Swagger UI to interact with the API and test the endpoints. You can access it at:

   [Swagger Documentation](http://auth.api.enviloup.localhost/docs)

### Environment Variables

The following environment variables need to be configured in the `docker-compose.yml` file or set in your local environment:

- `DATABASE__CONNECTIONSTRING`: Connection string for the PostgreSQL database, e.g.:

   ```shell
   DATABASE__CONNECTIONSTRING=Host=db;Port=5432;Database=auth_api;Username=postgres;Password=postgres
   ```

### Troubleshooting

- **Service startup issues**: If the service does not start, make sure the database container (`db`) is running and accessible.

- **Port conflicts**: Ensure that the ports you're using for the application (e.g., port 80 for NGINX or 8080 for the app) are not in use by other services on your machine.

---