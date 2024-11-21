# Face Comparison Project

Compare the similarity between two face images using deep learning.

---

## Prerequisites

- **Python** 3.9+
- **Node.js** 16+
- **npm** or **yarn**

---

## Backend Setup

### 1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install dependencies:

```bash
pip install torch torchvision facenet-pytorch fastapi python-multipart uvicorn pillow onnxruntime
```

### 3. Run the server:

```bash
uvicorn app:app --reload
```

The server runs at http://localhost:8000.

## Frontend Setup

### 1. Install dependencies:

```bash
npm install
```

### 2. Run the development server:

```bash
npm run dev
```

The frontend runs at http://localhost:5173.

## Usage

- Launch both the backend and frontend servers.
- Upload two face images through the interface.
- Click "Compare" to see the similarity percentage.
