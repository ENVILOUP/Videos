# Content service

The service provides content for users

[Swagger](http://api.enviloup.local:8080/content/docs)

## Development

Before work you need:

1. Docker and Docker compose installed

2. DNS records in the hosts file

```shell
# enviloup dev DNS records
127.0.0.1 enviloup.local
127.0.0.1 api.enviloup.local
127.0.0.1 cdn.enviloup.local
```

-----

1. Build 

```shell
docker compose build
```

2. Run for development

```shell
docker compose up -d
```

3. Open and make GET for [link](http://api.enviloup.local:8080/content/) and check
