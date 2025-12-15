Exporting models for Triton
==========================

This folder contains `export_and_triton.py` — a helper to export a detector to TorchScript and ONNX and produce a minimal Triton model repository layout.

Quick start
-----------

1. Install dependencies (example):

```powershell
pip install torch torchvision onnx requests
```

2. Export the baseline resnet-based detector to both TorchScript and ONNX:

```powershell
python backend\models\export_and_triton.py --model-name deepfake_detector --output-dir ./model_repository --format both
```

Using a pretrained deepfake model
---------------------------------

This script builds a `resnet18`-based detector by default and supports loading a checkpoint via `--weights-url`.
Provide a URL to a checkpoint (PyTorch `state_dict` or saved dict with `state_dict` key) to replace the weights before export.

Examples of where to obtain deepfake detection weights:
- Hugging Face model hub (search for "deepfake detector" or repository names like Xception-FaceForensics).
- Public GitHub releases for deepfake detection repositories (for example models trained on FaceForensics++).

Note: The repository does not ship third-party pretrained deepfake weights. After downloading a model checkpoint, re-run the export command with `--weights-url <url>` or download the file locally and update the script to point to the local file.

Triton layout produced
----------------------

The script will produce a layout like:

- `model_repository/<model_name>/1/model.pt` (TorchScript)
- `model_repository/<model_name>/config.pbtxt`
- `model_repository/<model_name>_onnx/1/model.onnx` (ONNX)
- `model_repository/<model_name>_onnx/config.pbtxt`

Adjust `config.pbtxt` to match your runtime (GPU instances, batching limits, model input names) if needed.
