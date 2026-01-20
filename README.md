# ReadSenseID-REST 

This software aims to providing REST and WebSocket interface to the RealSenseID library. 
It is meant to be a kickstarter for projects that utilize RealSenseID with remote access.

## Pre-requisites

- Python 3.14+
- uv (Python package and project manager)

## Installation - First Time

Install uv if you haven't already:

```shell
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Or see https://docs.astral.sh/uv/getting-started/installation/ for more installation options.

Standard installation (Linux & Windows):
```shell
uv sync                               # Install requirements
```

To install with development and test dependencies:
```shell
uv sync --extra dev --extra test     # Install all dependencies
```

## Update / Run

Update Packages (Linux & Windows):
```shell
uv sync                               # Install / Update requirements
```

Then everytime you need to run:
```shell
uv run poe run
```
or
```shell
uv run fastapi run rsid_rest/main.py
```
or
```shell
uv run python -m uvicorn rsid_rest.main:app --reload
```

## Usage
### API Documentation
Point your browser to: http://127.0.0.1:8000/docs/
### Sample Frontend
Point your browser to: http://127.0.0.1:8000/gui/

## Configuration and Settings
`.env` files and environment variables can be used to configura the application. The following table shows
the file names for environment files.

### Env files

| Environment |     File      |
|-------------|:-------------:|
| Dev         |    `.env`     |
| Prod        |  `prod.env`   |


### General Settings

The following variables can be set in the `.env` files or passed as Environment Variables before starting the app. 

| Variable                           | Default  | Configuration                                                                                            |
|------------------------------------|:--------:|----------------------------------------------------------------------------------------------------------|
| `auto_detect`                      |  `True`  | Automatically detect camera on system. Useful in dev environments                                        |
| `com_port`                         |  `None`  | Specifies COM port when `auto_detect` is False. Windows example: `COM5`                                  |
| `preview_camera_number`            |   `-1`   | Camera index for preview `-1` for auto-detect                                                            |
| `db_mode`                          | `device` | DB location: `device` or `host`                                                                          |

### Host DB Mode Settings

Similar to General Settings, the following variables can be set in `.env` or in the environment variables. They are only effective if `db_mode=host`

| Variable                           | Default  | Configuration                                                                                            |
|------------------------------------|:--------:|----------------------------------------------------------------------------------------------------------|
| `host_mode_auth_type`              | `hybrid` | In `host` DB mode: `hybrid`: use vector DB to enhance performance or: `device`: only use device matcher. |
| `host_mode_hybrid_max_results`     |   `10`   | In `host` and `hybrid`: Vector DB filters should filter for a max of X candidates                        |
| `host_mode_hybrid_score_threshold` |  `0.2`   | In `host` and `hybrid`: Vector DB filters should filter use this score threshold (keep low)              |


### Streaming Settings

Similar to General Settings, the following variables can be set in `.env` or in the environment variables.

| Variable                           | Default  | Configuration                                                                                            |
|------------------------------------|:--------:|----------------------------------------------------------------------------------------------------------|
| `preview_stream_type`              |  `jpeg`  | Streaming Preview output: `jpeg` or `webp`                                                               |
| `preview_jpeg_quality`             |   `85`   | Streaming Preview JPEG quality. Min: `1`     Max: `100`                                                  |
| `preview_webp_quality`             |   `85`   | Streaming Preview WebP quality. Min: `1`     Max: `100`                                                  |


### Creating a Client using the OpenAPI Schema
Running the following command will generate `openapi.json` file that can be used with the OpenAPI generator
```shell
uv run poe gen-openapi
```
Navigate to: https://github.com/OpenAPITools/openapi-generator?tab=readme-ov-file#overview to find out more about
the ability to automatically generate SDK that can use this API.

---
## Important Note
> End-user is responsible for providing the authentication and security mechanisms to protect access to the camera and RealSenseID API.
> Please refer to https://fastapi.tiangolo.com/tutorial/security/ for documentation on how to integrate authentication.
