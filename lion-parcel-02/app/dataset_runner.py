import os
import csv

from .blur import is_blurry
from .openai_client import describe_image

DATASET_DIR = "dataset"
OUTPUT_FILE = "output/results.csv"


def process_dataset() -> str:
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    results = []
    
    for filename in sorted(os.listdir(DATASET_DIR)):
        path = os.path.join(DATASET_DIR, filename)

        if not filename.lower().endswith((".jpg", ".jpeg", ".png")):
            continue

        with open(path, "rb") as img:
            image_bytes = img.read()

        try:
            if is_blurry(image_bytes):
                result = "blur"
            else:
                result = describe_image(image_bytes)
        except Exception as e:
            result = f"error: {str(e)}"

        results.append([filename, result])
        print(f"Processed {filename}: {result[:50]}...")

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["image_name", "result"])
        writer.writerows(results)

    return OUTPUT_FILE