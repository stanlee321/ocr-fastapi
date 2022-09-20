from typing import Optional
import uuid
from fastapi import FastAPI, File, HTTPException, Request
from cnocr import CnOcr
import PIL.Image as Image

import base64
import os
import io
import json
import numpy as np
# Some globals

app = FastAPI()

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            # 👇️ alternatively use str()
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)



@app.get("/")
def read_root():
    return {"Hello": "World"}


def save_image(base64_image, filename):
    """Save base64 image to file"""
    raw_img_data = base64.b64decode(base64_image)
    image = Image.open(io.BytesIO(raw_img_data))

    image.save(filename)


def load_model():
    rec_model_path = './models/cnocr'
    det_model_path = './models/cnstd'

    model = CnOcr(det_model_name='en_PP-OCRv3_det',
        rec_model_name='en_PP-OCRv3',
        rec_root=rec_model_path,
        det_root=det_model_path)

    return model

MODEL = load_model()


@app.post("/predict")
def predict(request: Request, img_bytes: bytes=File(...) ):

    data = {"success": False}

    uuid_name = str(uuid.uuid4())
    image_path = f"/tmp/{uuid_name}.jpg"
    
    # Save Image in /tmp
    save_image(img_bytes, image_path)
    
    try:
        
        out = MODEL.ocr(image_path)
        
        data["predictions"] = out
        data["success"] = True
        return {
            "data": json.dumps(data, cls=NpEncoder),
            "statusCode": 200
        }

    except Exception as e:
        print(e)
        data["error"] = str(e)
        return {
            "data": json.dumps(data, cls=NpEncoder),
            "statusCode": 500
        }


if __name__ == "__main__":
    import os
    from fastapi.testclient import TestClient

    tc = TestClient(app)
    
    URL = 'http://localhost:8002/predict'

    with open('test/impuestos.jpeg', "rb") as image_file:
        base64_image = base64.b64encode(image_file.read())

    # Setup separate json data
    payload = {
        "mime" : "image/png",
        "img_bytes": base64_image,
    }


    response = tc.post("/predict", data= payload)

    print(response.json())