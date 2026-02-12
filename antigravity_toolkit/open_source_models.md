# Hunyuan 3D (Open Source) - Local Deployment Guide

This guide explains how to set up and use Tencent's Hunyuan 3D model locally for free, unlimited 3D asset generation.

## 📋 Requirements

*   **OS:** Linux (Recommended) or Windows with WSL2.
*   **GPU:** NVIDIA GPU with at least 6GB VRAM (12GB+ Recommended for best performance).
*   **Software:** Python 3.9+, CUDA Toolkit 11.8+, PyTorch.

## 🚀 Installation Steps

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/Tencent/Hunyuan3D
    cd Hunyuan3D
    ```

2.  **Create Virtual Environment:**
    ```bash
    conda create -n hunyuan3d python=3.9
    conda activate hunyuan3d
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Download Pre-trained Models:**
    Download the model weights from Hugging Face:
    *   `Tencent/Hunyuan3D-1` (or latest version)
    Place them in the `weights/` directory.

## 🎨 Usage (Inference)

### Text-to-3D
Generate a 3D model from a text prompt.

```bash
python inference.py \
    --prompt "a futuristic cyberpunk motorcycle" \
    --output_dir ./outputs \
    --format obj
```

### Image-to-3D
Generate a 3D model from a single image.

```bash
python inference.py \
    --image_path ./input_image.png \
    --output_dir ./outputs \
    --format glb
```

## 🛠️ Integration with Workflows

*   **Blender:** Use the generated `.obj` or `.glb` files directly in Blender.
*   **Game Engines:** Import assets into Unity or Unreal Engine for prototyping.
*   **3D Printing:** Ensure the mesh is "watertight" (manifold) using tools like MeshLab before printing.

## ⚠️ Troubleshooting

*   **OOM Errors (Out of Memory):** Reduce batch size or resolution if you have limited VRAM.
*   **Artifacts:** Try different seeds or refine the text prompt for better results.
