# Video-Upload-and-Subtitle-Extraction

# Multilingual Video Upload and Subtitle Extraction Platform

This project is a video processing web application that allows users to upload videos, extract subtitles in multiple languages using `ffmpeg`, and search for specific phrases within the video. Users can view timestamps for searched phrases and jump to specific points in the video where they occur. The project is containerized using Docker for easy setup and management.

## Features

- **Video Upload**: Users can upload video files for processing.
- **Subtitle Extraction**: Subtitles are extracted using `ffmpeg` and displayed as closed captions. Multi-language subtitles are supported.
- **Search Functionality**: Users can search for specific phrases within the video subtitles, and the video will jump to the timestamp of the searched phrase.
- **List View**: Uploaded videos are listed, and users can view videos and corresponding subtitles.
- **Docker Support**: The application is fully containerized using Docker and `docker-compose`, ensuring easy setup and consistent environments.
  
## Tech Stack

- **Backend**: Django (Python)
- **Database**: PostgreSQL
- **Video Processing**: ffmpeg (for subtitle extraction)
- **Containerization**: Docker, Docker Compose

## Requirements

- [ffmpeg](https://ffmpeg.org/download.html) (for subtitle extraction)
- Docker and Docker Compose (for containerization)

## Setup Instructions

1. **Clone the Repository**:
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2. **Download and Install ffmpeg**:
   Download and install ffmpeg from [here](https://ffmpeg.org/download.html). Ensure `ffmpeg` is accessible from your system's PATH.

3. **Docker Setup**:
   Make sure you have Docker and Docker Compose installed on your machine. You can follow the official installation guides:
   - [Docker Installation Guide](https://docs.docker.com/get-docker/)
   - [Docker Compose Installation Guide](https://docs.docker.com/compose/install/)

4. **Configure Environment Variables**:
    Create a `.env` file in the root directory of your project and add the following configurations:
    ```ini
    DEBUG=1
    SECRET_KEY=your_secret_key
    DATABASE_NAME=your_db_name
    DATABASE_USER=your_db_user
    DATABASE_PASSWORD=your_db_password
    DATABASE_HOST=db
    DATABASE_PORT=5432
    ```

5. **Run the Application**:
    Use `docker-compose` to build and run the application:
    ```bash
    docker-compose up --build
    ```

    This will start the Django backend, PostgreSQL database, and any other services needed.

6. **Access the Application**:
    Once the application is running, you can access it via:
    ```
    http://localhost:8000
    ```

## Usage

1. **Upload a Video**: 
   Navigate to the upload page and upload a video file. The video will be processed in the background, and subtitles will be extracted.

2. **View Subtitles**: 
   Once the subtitles are extracted, they will be displayed as closed captions alongside the video.

3. **Search for a Phrase**:
   Use the search functionality to find a specific phrase in the subtitles. The video will jump to the exact point where the phrase appears.

4. **List View**: 
   View the list of all uploaded videos, select any video to view its subtitles and perform searches.

## Project Structure

```bash
├── app
│   ├── Dockerfile          # Dockerfile for Django backend
│   ├── manage.py           # Django project management file
│   ├── app                 # Django app containing views, models, and other logic
├── db
│   ├── Dockerfile          # Dockerfile for PostgreSQL database
│   ├── init.sql            # SQL initialization script for the database
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
