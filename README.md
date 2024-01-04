# imagesim

A microservice for embedding images and finding nearest neighbors.

## Installation

To install `imagesim`, you can either use [Poetry](https://python-poetry.org/) to install the project dependencies, or you can use the provided Dockerfile to build a Docker image.

### Poetry
Install Poetry using the instructions on their website. Then, run the following commands to install the project dependencies and start the server.
```bash
poetry install
cd src # uvicorn needs to be run from where the app is
uvicorn --reload main:app 
```

### Docker
The Dockerfile is configured as a multi-stage build with development and production stages. To build the development image, run the following command from the root of the project.
```bash
docker build --target development -t imagesim:dev .
```
The development image does not include the project source code so that code changes do not require rebuilding the image. To run the development image, you must mount the source code as a volume.
```bash
docker run -p 8000:8000 -v ./src:/app imagesim:dev
```
Each time you make a change to the source code, the server will automatically restart. If you need to install additional dependencies, you will need to do that using Poetry and then rebuild the image.

## Usage
Documentation for the API is available at `/docs` or `/redoc` when the server is running. `/docs` provides a more interactive experience (e.g. you can try out the API directly from the browser), while `/redoc` provides a more readable 2-column layout.

## Testing
TODO.

## Deployment
Build the production image using the following command.
```bash
docker build --target production -t imagesim:prod .
```
The production image includes the project source code, so you do not need to mount a volume when running it.
```bash
docker run -p 8000:8000 imagesim:prod
```