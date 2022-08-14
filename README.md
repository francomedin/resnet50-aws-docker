# Flask ML API

## Install and run

To run the services using compose:

```bash
$ docker-compose up --build -d
```

To stop the services:

```bash
$ docker-compose down
```

## Tests

### Integration end-to-end

You must have the full pipeline running and [requests](https://docs.python-requests.org/en/latest/) library installed. Then, from this project root folder run:

```
$ python tests/test_integration.py
```

### Modules

We make use of [multi-stage docker builds](https://docs.docker.com/develop/develop-images/multistage-build/) so we can have into the same Dockerfile environments for testing and also for deploying our service.

#### Api

Run:

```bash
$ cd api/
$ docker build -t flask_api_test --progress=plain --target test .
```

You will only need to pay attention to the logs corresponding to the testing code which will look like this:

```bash

#### Model

Same as api, run:

```bash
$ cd model/
$ docker build -t model_test --progress=plain --target test .
```
