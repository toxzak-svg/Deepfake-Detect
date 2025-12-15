# GPU Serving & Production Model Deployment

Options for serving models with GPU acceleration:

- NVIDIA Triton Inference Server: supports PyTorch, TensorRT, ONNX. Use Triton for high-throughput, production inference and autoscaling.
- TorchServe: simpler PyTorch-native model serving with REST/gRPC endpoints.
- Custom FastAPI + CUDA-ready Docker image: for lightweight deployments.

Notes:
- Use a CUDA-enabled base image (e.g., `nvidia/cuda:12.1-runtime-ubuntu22.04`) when building GPU containers.
- Ensure drivers and the NVIDIA Container Toolkit are installed on the host.
- Convert models to optimized formats (TorchScript, ONNX, TensorRT) for lower latency.

Example: Dockerfile (outline) for TorchServe

```dockerfile
FROM pytorch/torchserve:latest
COPY model-store /home/model-server/model-store
EXPOSE 8080 8081
CMD ["torchserve", "--start", "--model-store", "/home/model-server/model-store", "--models", "deepfake=deepfake.mar"]
```

Example: using Triton with a PyTorch model
- Export PyTorch model to TorchScript or ONNX and place under Triton model repo structure.
