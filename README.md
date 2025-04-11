# django-unpoly-playground

An opinionated boilerplate project using Django with Vite for js/css assets and a dockerized development environment + production-ready docker image for deployment.

- Django 5.1
- Python 3.13
- Postgres 17
- Docker Compose for local development
- Dockerfile for building a production-ready image
- Vite for frontend assets (see unpoly, alpine and tailwind implemented as examples)
- Justfile recipes
- uv for package and project management
- ruff, pytest, django-environ, and many more nice tools


## Get Started
This project leverages [uv](https://docs.astral.sh/uv/getting-started/installation/), [just](https://github.com/casey/just) and [Docker Compose](https://docs.docker.com/compose/install/) for managing the development environment. Make sure you have installed he necessary dependencies for running them on your local machine.

Initialize the dev environment with the `just bootstrap` recipe. This will build the dev image and prepare everything before you can start the app and the dependant infrastructure services with the `just start` recipe. Stop all services with hitting `CTRL+C` or using the `just stop` recipe in another terminal. 

```sh
just bootstrap
just start
```

## Usage
The most used project commands are available as just recipe:
```shell
just [recipe]
```

```make
Available recipes:
    bootstrap *ARGS   # bootstrap project
    build *ARGS       # build project
    start *ARGS       # start project
    stop *ARGS        # stop project
    infra-start *ARGS # start infra services
    infra-stop *ARGS  # stop infra services
    app-start *ARGS   # start django app
    app-stop *ARGS    # start django app
    run *ARGS         # uv run command in container
    manage *ARGS      # run django management command
    env               # copy .env.example to .env if not exists
    pre *ARGS         # run pre-commit processes
    ruff *ARGS        # run ruff linting & formatting
    test *ARGS        # run tests
    test-cov *ARGS    # run tests with coverage
    clean *ARGS       # clean up cache files etc.
```

## Project Structure

### Core Directories

- `/src`: Contains the Django project and apps
  - `/apps`: Contains all Django applications
    - `/demo`: Example demo application with team management functionality
  - `/config`: Django project configuration
    - `/settings`: Environment-specific Django settings
      - `base.py`: Base settings shared across all environments
      - `dev.py`: Development environment settings
      - `prod.py`: Production environment settings
      - `test.py`: Test environment settings
  - `/templates`: Project-wide templates
    - `/cotton`: Component templates for consistent UI

- `/assets`: Frontend assets managed by Vite
  - `/css`: Stylesheets (Tailwind config/theme goes here)
  - `/js`: JavaScript files including Alpine.js and Unpoly

### Unpoly Integration

This project uses [Unpoly](https://unpoly.com/), a framework for making web applications feel faster by avoiding full page reloads. Key features:

- AJAX navigation without writing JavaScript
- Progressive enhancement
- Smooth page transitions
- Server-rendered HTML

The Unpoly middleware is configured in `src/config/settings/base.py` and the JavaScript is included in `/assets/js/unpoly.js`.

### Environment Variables

The project uses django-environ to manage environment variables. Create a `.env` file in the project root (use `just env` to create one from the example file) with the following variables:

```
# Django
DEBUG=True
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgres://postgres:postgres@postgres:5432/postgres

# Deployment
DJANGO_SETTINGS_MODULE=config.settings.dev
```

### Creating New Apps

To create a new Django app:

```sh
just manage startapp my_app src/apps/my_app
```

Then:
1. Add your app to `INSTALLED_APPS` in `src/config/settings/base.py`
2. Create templates in `src/apps/my_app/templates/`
3. Create URL patterns in `src/apps/my_app/urls.py`
4. Include your app's URLs in `src/config/urls.py`

## Template Structure

The project uses a hierarchical template structure:

- `base.html`: The main template that all pages extend
- `/cotton`: UI components inspired by the [Cotton Design System](https://cotton.tuk.dev/)
  - `/form`: Form-specific components
  - `/layout`: Layout templates
  - `/section`: Content section components

## Development Workflow

1. Run `just start` to start all services
2. Make changes to your code - Django's development server will auto-reload
3. Run `just test` to execute tests
4. Run `just ruff` to check code style and formatting

## Production Deployment

Build the production image:
```sh
just build
```

The production configuration:
- Collects static files
- Uses Django's production settings
- Runs with gunicorn as the WSGI server

Deploy using your preferred container orchestration platform.

## Acknowledgement
This boilerplate is inspired by [Nick Janetakis' docker-django-example](https://github.com/nickjj/docker-django-example) and [Jeff Triplett's django-startproject](https://github.com/jefftriplett/django-startproject/). I used a lot of patterns, practices and also code snippets from their projects. I highly recommend taking a look at their repos as it may be more usefull. This boilerplate is an opinionated copy/mix of their work to make it fit my personal needs.