from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import onnxruntime as ort
from PIL import Image
import io
import torch
import torch.nn.functional as F
from facenet_pytorch import MTCNN

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mtcnn = MTCNN(keep_all=False)
session = ort.InferenceSession("facenet.onnx")


def process_image(image_bytes):
    img = Image.open(io.BytesIO(image_bytes)).convert('RGB')
    face = mtcnn(img)
    if face is None:
        raise ValueError("No face detected")
    face = face.unsqueeze(0)
    return face.numpy()


@app.post("/compare")
async def compare_faces(image1: UploadFile, image2: UploadFile):
    try:
        img1_bytes = await image1.read()
        img2_bytes = await image2.read()

        face1 = process_image(img1_bytes)
        face2 = process_image(img2_bytes)

        embedding1 = session.run(None, {"input": face1})[0]
        embedding2 = session.run(None, {"input": face2})[0]

        emb1_tensor = F.normalize(torch.tensor(embedding1), p=2, dim=1)
        emb2_tensor = F.normalize(torch.tensor(embedding2), p=2, dim=1)

        similarity = F.cosine_similarity(emb1_tensor, emb2_tensor).item() * 100

        return {"similarity": round(similarity, 2)}
    except ValueError as e:
        return {"error": str(e)}, 400