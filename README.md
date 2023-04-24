# ProjectAlpha

## Setup

### Python

The application is built using `python 3.8.10`

### Installing requirements

Move to bakcend directory:

```
cd backend
```

In the backend directory run:

```
pip install -r requirements.txt
```

### libvoikko

You also need to have `libvoikko` installed on your environment.

#### macOS

```
brew install libvoikko
```

#### linux

```
apt-get update && apt-get install -y voikko-fi python-libvoikko
```

#### windows

In lemmatizer.py file comment out the following line:

```
v = Voikko("fi")
```

uncomment the following lines:

```
Voikko.setLibrarySearchPath("./Voikko")
v = Voikko(language="fi", path="./Voikko")

```

## Running the application

### locally

in backend directory run

```
py backend.py
```

### Docker

in backend directory run:

```
docker build -t backend .
```

Then the application can be run with:

```
docker run -p 5000:5000 backend
```

## Swagger

Swagger dovumentation is in path `/apidocs/#/`

e.g. when run locally: `http://localhost:5000/apidocs/#/`

## Front-end application for testing

### Setup

Move to frontend directory:

```
cd frontend
```

In the frontend directory run:

```
npm install
```

### Running the frontend application

In the frontend directory run:

```
npm start
```

## docker compose

If you want to deploy both frontend and backend using docker, in root directory run:

```
docker compose up --build
```
