# Content service

The service provides content for users

[Swagger](http://content.api.enviloup.localhost/docs)

# To run tests

```shell
docker compose exec -it content-app pytest -vvv --cov=/app --cov-report=term-missing
```
