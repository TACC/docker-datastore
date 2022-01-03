# Sample `docker-compose` With Datastore and Client

This application demonstrates a data store container and a client, which is a Dash application

## Containers

There are two containers in this application:

- `datastore` is a container accessible only within the Docker network that exposes a `/api` endpoint and returns json data
- `datastore_client` is a container that requests data from `datastore`, and surfaces a Dash application

## Running

You can run this application with `docker-compose -f docker-compose.dev.yml up`. This compose file also has both containers set to live reload with source mounting, for live development.