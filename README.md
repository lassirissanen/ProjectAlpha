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

#### Note on macOS

You need to change the `tensorflow==2.11.0` requirement to `tensorflow-macos==2.11.0`

### libvoikko

You also need to have `libvoikko` installed on your environment.

#### macOS

```
brew install libvoikko
```

Also with macOS, in lemmatizer.py file uncomment the following line:

```
v = Voikko("fi")
```

and comment out the following lines:

```
Voikko.setLibrarySearchPath("./Voikko")
v = Voikko(language="fi", path="./Voikko")

```

#### linux

```
apt-get update && apt-get install -y voikko-fi python-libvoikko
```

#### windows

The project has the libvoikko dll library in the `backend/Voikko` directory so no need to install it.

## Running the backend application

### locally

in backend directory run

```
py backend.py
```

## Training the TensorFlow model

The model is trained when the backend server is started or the `backend/tensorflow_classifier.py` file is run. After that the model is saved in generated `backend/models` directory and loaded from there when the server is started after the first time. If you want to retrain the model, delete the generated
`backend/models` directory and start the server again.

### Modifying the training data

The training data for the TensorFlow model is located in `backend/responses.csv` file. To modify the training data you can modify that file and the retrain the model. Remember to delete the `backend/models` directory.

### Structure of the responses.csv file

There should be 2 columns "response" and "class". The delimeter is comma "," so if the response contains any commas the response should be inside quotations e.g. "moi, ei käy". The options for class column are currently accept, decline and suggestion.

## Swagger

Swagger dovumentation can be found in path `/apidocs/#/`

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

## Docker

in backend directory run:

```
docker build -t backend .
```

Then the application can be run with:

```
docker run -p 5000:5000 backend
```

NOTE: to change the port e.g. to 8080 you can do

```
-p 8080:5000
```

### docker compose

If you want to run both frontend and backend using docker, in root directory run:

```
docker compose up
```

Rebuilding the docker compose can be done with:

```
docker compose up --build
```

NOTE: When running with docker compose, the frontend path will be `8080:/` and the backend will be `8080:/api`
