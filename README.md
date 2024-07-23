## Video Processing and Audio Generation Application
### This application allows you to split videos into parts, generate audio from text prompts, and add the generated audio to specific video parts. It is built using Streamlit for the user interface and includes functionality for video manipulation and audio generation.

### Table of Contents
Installation
Usage
Running with Docker
License
### Installation
### Prerequisites
Before setting up the project, ensure you have Poetry installed. You can install Poetry using the following command:

```

pip install poetry

```
### Installing Dependencies
1) Clone the repository:

```

git clone https://github.com/Sampleeeees/video_splitter.git

```
```

cd video_splitter

```

2) Install the project dependencies using Poetry:

```

poetry install

```

## Usage
### Running Locally
To run the application locally:

```

streamlit run app.py

```
This will start the Streamlit server, and you can access the application by navigating to http://localhost:8501 in your web browser.


## Running with Docker
### To build and run the application using Docker:

```

docker compose up --build

```
This will start the application inside a Docker container and map port 8501 on your host to port 8501 in the container. You can access the application by navigating to http://localhost:8501 in your web browser.
