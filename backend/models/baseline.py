"""Pretrained-model based detector scaffold.

Uses a torchvision `resnet18` pretrained on ImageNet as a feature extractor.
For demo purposes we compute a simple score from the feature vector magnitude.
Replace with a trained deepfake classifier for production.
"""
from typing import List
import torch
import numpy as np


class BaselineDetector:
    def __init__(self, device: str | None = None):
        if device is None:
            device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = torch.device(device)
        try:
            import torchvision.models as models
            import torchvision.transforms as T

            self.transforms = T.Compose([
                T.ToPILImage(),
                T.Resize((224, 224)),
                T.ToTensor(),
                T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
            ])
            # load pretrained resnet18 and take features before final fc
            resnet = models.resnet18(pretrained=True)
            modules = list(resnet.children())[:-1]
            self.feature_extractor = torch.nn.Sequential(*modules).to(self.device)
            self.feature_extractor.eval()
        except Exception:
            # fallback to a tiny random model if torchvision not available
            self.transforms = None
            self.feature_extractor = None

    def _score_from_feature(self, feat: torch.Tensor) -> float:
        # simple scoring heuristic: normalized L2 magnitude mapped to [0,1]
        v = feat.detach().cpu().numpy().ravel()
        mag = float(np.linalg.norm(v))
        # heuristic mapping
        score = 1.0 / (1.0 + np.exp(-0.01 * (mag - 10.0)))
        return float(score)

    def predict_frames(self, frames: List[np.ndarray]) -> List[float]:
        out = []
        if self.feature_extractor is None:
            # fallback: return small random scores
            for _ in frames:
                out.append(0.1)
            return out

        with torch.no_grad():
            for f in frames:
                arr = f.astype(np.uint8)
                if self.transforms is not None:
                    x = self.transforms(arr).unsqueeze(0).to(self.device)
                else:
                    # naive resize & normalize
                    import cv2

                    arr = cv2.resize(arr, (224, 224)).astype(np.float32) / 255.0
                    x = torch.from_numpy(arr).permute(2, 0, 1).unsqueeze(0).to(self.device)
                feat = self.feature_extractor(x)
                # feat shape: (1, C, 1, 1)
                s = self._score_from_feature(feat)
                out.append(s)
        return out


if __name__ == "__main__":
    import numpy as np

    detector = BaselineDetector()
    dummy = [np.zeros((224, 224, 3), dtype=np.uint8)]
    print(detector.predict_frames(dummy))
