# The Weather API

---

This Weather API searches for weather stations for a given location and returns weather data for a chosen station.
The API is built using Python, Django and Django Rest Framework.

---

## Run it locally

### How to - Local

To build and rund the app locally, run:

```bash
Mac: source/vevn/bin/activate
Windows: venv\Scripts\activate
```

```bash
python manage.py runserver
```

---

## Run the container

### Prerequisites - Container

- Docker

### How to - Container

To pull and run the container, run:

```bash
docker run -p 8000:8000 ghcr.io/weathercrew/weather-api:latest
```

---

## Further Information

API Documentation can be found at: [docs/api_documentation.md](docs/api_documentation.md) 
To see the other part of the application, visit the [Frontend Repo](https://github.com/WeatherCrew/weather-ui)



