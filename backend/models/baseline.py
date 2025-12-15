"""Baseline model scaffolding for image/video classification.

This is a lightweight entrypoint demonstrating how to load a model and run
inference over frames. Replace with production training/inference code.
"""
from typing import List
import torch
import numpy as np


class BaselineDetector:
    def __init__(self, device: str = "cpu"):
        self.device = torch.device(device)
        # small random model for scaffold
        self.model = torch.nn.Sequential(
            torch.nn.Flatten(),
            torch.nn.Linear(224 * 224 * 3, 128),
            torch.nn.ReLU(),
            torch.nn.Linear(128, 1),
            torch.nn.Sigmoid(),
        ).to(self.device)

    def predict_frames(self, frames: List[np.ndarray]) -> List[float]:
        self.model.eval()
        out = []
        with torch.no_grad():
            for f in frames:
                # expect uint8 HWC
                arr = f.astype(np.float32) / 255.0
                if arr.shape != (224, 224, 3):
                    # naive resize
                    import cv2

                    arr = cv2.resize(arr, (224, 224))
                x = torch.from_numpy(arr).permute(2, 0, 1).unsqueeze(0)
                x = x.to(self.device)
                x = x.view(1, -1)
                p = self.model(x).item()
                out.append(p)
        return out


if __name__ == "__main__":
    import numpy as np

    # quick smoke test
    detector = BaselineDetector()
    dummy = [np.zeros((224, 224, 3), dtype=np.uint8)]
    print(detector.predict_frames(dummy))
