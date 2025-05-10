![enviloup logo](./docs/assets/logo/enviloup_logo.png)

# Enviloup Videos


Streaming media service like YouTube

## Roadmap (MVP)

- Streaming video and streams
- Reactions: likes, dislikes
- User viewing history
- Simple search and filtering
- Video feed and subscriptions
- Make a service for recommendations (mocks for now)
- Admin panel for moderators
- Studio for authors
- Authorization (simple and *Oauth2)
- Write a front that you won't be ashamed to show to the guys

# How to run?

To start backend use:

```shell
docker compose -f docker-compose.yml up -d
```

If you run first time then you must run with `--build` argument

# Development

To develop a specific service, you can read the instructions from the README in the folder.

To start backend in development mode use:

```shell
docker compose up -d
```
