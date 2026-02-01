from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import requests
import os

from .blur import is_blurry
from .openai_client import describe_image
from .dataset_runner import process_dataset

app = FastAPI(title="Image Analyzer API")

app.mount(
    "/images",
    StaticFiles(directory="static/images"),
    name="images"
)


class ImageRequest(BaseModel):
    image_url: str


@app.post("/analyze-image")
def analyze_image(payload: ImageRequest):
    image_url = payload.image_url

    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(image_url, headers=headers, timeout=10)
        response.raise_for_status()
        image_bytes = response.content
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Failed to fetch image: {e}")

    try:
        if is_blurry(image_bytes):
            return {"result": "blur"}

        description = describe_image(image_bytes)
        return {"result": description}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {e}")


@app.post("/process-dataset")
def run_dataset_processing():
    try:
        output_path = process_dataset()
        return {"status": "success", "output_file": output_path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing dataset: {e}")


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
