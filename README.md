# django-vite-example

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

## Asset Pipeline

The project uses Vite to manage and build frontend assets, including JavaScript, CSS, and other static files. The asset pipeline is integrated into the Dockerized environment for both development and production.

### Development Workflow

1. **Asset Development Server**: During development, the `assets` service in `docker-compose.yml` runs the Vite development server. This allows for hot module replacement (HMR) and live reloading of frontend assets.
   - Command: `pnpm run dev`
   - Port: `${DJANGO_VITE_DEV_SERVER_PORT}` (default: 5175)

2. **File Structure**:
   - `/assets/js`: Contains JavaScript files, including `alpine.js` and `unpoly.js`.
   - `/assets/css`: Contains Tailwind CSS configuration and custom styles.
   - `/assets/package.json`: Defines dependencies and scripts for the asset pipeline.

3. **Running Locally**:
   - Start the development server with `just start`. The Vite server will serve assets dynamically.

### Production Workflow

1. **Asset Build**: The `assets_builder` stage in the `Dockerfile` compiles and bundles the assets using Vite.
   - Command: `pnpm run build`
   - Output: Bundled assets are placed in `/app/src/assets_dist`.

2. **Static File Collection**: During the production build, Django collects the static files, including the compiled assets, into the `staticfiles` directory.
   - Command: `python3 manage.py collectstatic --no-input`

3. **Docker Integration**:
   - The `assets` service in `docker-compose.yml` ensures that assets are built and served correctly.
   - The production image includes pre-built assets for deployment.

### Production Usage

In a production environment, Docker Compose is not used. Instead, the production Docker image should be built and deployed using the default target in the `Dockerfile`. The following steps outline the production workflow:

1. **Build Production Image**:
   - Use the default target in the `Dockerfile` to build the production-ready image.
   - Command:
     ```sh
     docker build -t your-production-image-name .
     ```

2. **Deploy the Image**:
   - Deploy the built image using your preferred container orchestration platform (e.g., Kubernetes, Docker Swarm).
   - Ensure that the `DJANGO_SETTINGS_MODULE` environment variable is set to `config.settings.prod` for production settings.

3. **Static File Collection**:
   - The production image automatically collects static files during the build process using the `collectstatic` command.

4. **Environment Variables**:
   - Configure the necessary environment variables for production, such as `SECRET_KEY`, `DATABASE_URL`, and `ALLOWED_HOSTS`.

### Development vs Production Targets

- **Development**:
  - Use the `app_dev` target in the `Dockerfile` for development.
  - This target includes tools and configurations for debugging and live reloading.
  - Command:
    ```sh
    docker-compose up
    ```

- **Production**:
  - Use the default target in the `Dockerfile` for production.
  - This target is optimized for performance and excludes development dependencies.
  - Command:
    ```sh
    docker build -t your-production-image-name .
    ```

### pnpm as Default Package Manager

This project uses `pnpm` as the default package manager for managing frontend dependencies. It is chosen for its speed, efficient disk space usage, and monorepo support.

### Environment Variables

The following environment variables control the asset pipeline:

- `NODE_ENV`: Set to `development` for local development and `production` for builds.
- `DJANGO_VITE_DEV_MODE`: Set to `true` for development mode and `false` for production.
- `DJANGO_VITE_DEV_SERVER_PORT`: Port for the Vite development server (default: 5175).

This setup ensures a seamless integration of the asset pipeline into the Django project, providing a modern frontend development experience.

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