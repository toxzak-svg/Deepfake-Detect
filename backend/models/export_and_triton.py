"""Export a detector to TorchScript and ONNX and create a Triton model repo layout.

Usage examples:
  python export_and_triton.py --model-name deepfake_detector --output-dir model_repository --format both

You can supply `--weights-url` to download a checkpoint (expects a PyTorch state_dict or checkpoint).
"""
from __future__ import annotations

import argparse
import os
import tempfile
from pathlib import Path
import requests
import torch


def build_resnet_detector(device: torch.device = None) -> torch.nn.Module:
    import torchvision.models as models

    model = models.resnet18(pretrained=True)
    num_features = model.fc.in_features
    model.fc = torch.nn.Sequential(torch.nn.Linear(num_features, 1), torch.nn.Sigmoid())
    return model


def download_url(url: str, dst: Path) -> Path:
    resp = requests.get(url, stream=True)
    resp.raise_for_status()
    with open(dst, "wb") as f:
        for chunk in resp.iter_content(1024 * 1024):
            if chunk:
                f.write(chunk)
    return dst


def save_torchscript(model: torch.nn.Module, save_path: Path, device: torch.device):
    model.eval()
    example = torch.randn(1, 3, 224, 224, device=device)
    traced = torch.jit.trace(model.to(device), example)
    traced.save(str(save_path))


def save_onnx(model: torch.nn.Module, save_path: Path, device: torch.device):
    model.eval()
    example = torch.randn(1, 3, 224, 224, device=device)
    torch.onnx.export(
        model.to(device),
        example,
        str(save_path),
        export_params=True,
        opset_version=11,
        input_names=["input"],
        output_names=["output"],
        dynamic_axes={"input": {0: "batch"}, "output": {0: "batch"}},
    )


def make_triton_config(model_name: str, platform: str, filename: Path):
    # minimal Triton config; adjust gpu/instance_group etc. as needed
    cfg = f"""
name: "{model_name}"
platform: "{platform}"
max_batch_size: 8
input [
  {{
    name: "input"
    data_type: TYPE_FP32
    format: FORMAT_NCHW
    dims: [3, 224, 224]
  }}
]
output [
  {{
    name: "output"
    data_type: TYPE_FP32
    dims: [1]
  }}
]
"""
    filename.write_text(cfg.strip() + "\n")


def prepare_model_repo(model_name: str, output_dir: Path, save_torch: bool, save_onnx: bool, device: torch.device):
    output_dir.mkdir(parents=True, exist_ok=True)
    if save_torch:
        repo = output_dir / model_name
        model_version_dir = repo / "1"
        model_version_dir.mkdir(parents=True, exist_ok=True)
        pt_path = model_version_dir / "model.pt"
        print("Saving TorchScript to", pt_path)
        model = build_resnet_detector(device=device)
        save_torchscript(model, pt_path, device)
        make_triton_config(model_name, "pytorch_libtorch", repo / "config.pbtxt")

    if save_onnx:
        repo = output_dir / (model_name + "_onnx")
        model_version_dir = repo / "1"
        model_version_dir.mkdir(parents=True, exist_ok=True)
        onnx_path = model_version_dir / "model.onnx"
        print("Saving ONNX to", onnx_path)
        model = build_resnet_detector(device=device)
        save_onnx(model, onnx_path, device)
        make_triton_config(model_name + "_onnx", "onnxruntime_onnx", repo / "config.pbtxt")


def try_load_weights(model: torch.nn.Module, ckpt_path: Path):
    # load a state_dict if possible
    try:
        ckpt = torch.load(str(ckpt_path), map_location="cpu")
        if isinstance(ckpt, dict) and "state_dict" in ckpt:
            state = ckpt["state_dict"]
        elif isinstance(ckpt, dict) and all(isinstance(k, str) for k in ckpt.keys()):
            # likely a state_dict
            state = ckpt
        else:
            # fallback, try loading directly
            state = ckpt
        model.load_state_dict(state)
        print("Loaded weights into model from", ckpt_path)
    except Exception as e:
        print("Warning: failed to load checkpoint:", e)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model-name", default="deepfake_detector")
    parser.add_argument("--output-dir", type=Path, default=Path("model_repository"))
    parser.add_argument("--format", choices=["torchscript", "onnx", "both"], default="both")
    parser.add_argument("--device", default=None, help="cpu or cuda")
    parser.add_argument("--weights-url", default=None, help="optional URL to a PyTorch checkpoint (state_dict)")
    args = parser.parse_args()

    device = torch.device(args.device if args.device is not None else ("cuda" if torch.cuda.is_available() else "cpu"))

    # If weights URL provided, download to a temp file and attempt to load while building
    tmp_ckpt = None
    if args.weights_url:
        tmpf = Path(tempfile.gettempdir()) / f"{args.model_name}.ckpt"
        print("Downloading weights from", args.weights_url)
        download_url(args.weights_url, tmpf)
        tmp_ckpt = tmpf

    save_torch = args.format in ("torchscript", "both")
    save_onnx = args.format in ("onnx", "both")

    # If a specific weights file was downloaded, pass to loader function
    # Our simple builder uses torchvision resnet; to apply checkpoint, we build model and then try load weights
    if tmp_ckpt is not None:
        global build_resnet_detector
        m = build_resnet_detector(device=device)
        try_load_weights(m, tmp_ckpt)
        # save modified model into a temporary place and export from it
        # overwrite the builder functions to return our loaded model
        def _loaded_builder(device: torch.device = None):
            return m

        build_resnet_detector = _loaded_builder

    prepare_model_repo(args.model_name, args.output_dir, save_torch, save_onnx, device)


if __name__ == "__main__":
    main()
