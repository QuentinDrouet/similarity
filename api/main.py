import torch
import torch.nn.functional as F
from facenet_pytorch import InceptionResnetV1, MTCNN
from PIL import Image
import onnxruntime as ort

feature_extractor = InceptionResnetV1(pretrained='vggface2').eval()
mtcnn = MTCNN(keep_all=False)


def preprocess_image(image_path):
    img = Image.open(image_path).convert('RGB')
    face = mtcnn(img)
    if face is None:
        raise ValueError(f"No face detected in image: {image_path}")
    return face.unsqueeze(0)


def compute_similarity(feature_extractor, img1, img2):
    with torch.no_grad():
        embedding1 = feature_extractor(img1)
        embedding2 = feature_extractor(img2)

        embedding1 = F.normalize(embedding1, p=2, dim=1)
        embedding2 = F.normalize(embedding2, p=2, dim=1)

        similarity = F.cosine_similarity(embedding1, embedding2)
        return similarity.item()


def export_to_onnx(model, onnx_path):
    dummy_input = torch.randn(1, 3, 160, 160)
    torch.onnx.export(
        model,
        dummy_input,
        onnx_path,
        input_names=['input'],
        output_names=['embedding'],
        opset_version=11
    )
    print(f"Model exported to {onnx_path}")


def run_onnx_model(onnx_path, img):
    session = ort.InferenceSession(onnx_path)
    inputs = {session.get_inputs()[0].name: img.numpy()}
    outputs = session.run(None, inputs)
    return outputs[0]


def main():
    export_to_onnx(feature_extractor, "facenet.onnx")


if __name__ == "__main__":
    main()
