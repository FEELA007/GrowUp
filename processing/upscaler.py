from pathlib import Path
import cv2
import torch
from  basicsr.archs.rrdbnet_arch import RRDBNet
from realesrgan import RealESRGANer
Model_PATH=(Path(__file__).resolve().parent.parent/ "models" / "RealESRGAN_x4plus.pth")

_model=None
def get_upscaler():
    global _model
    if _model is not  None:
        return _model
    if not Model_PATH.exists():
        raise FileNotFoundError(f"Real-ESRGAN model file not found:\n{Model_PATH}")
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = RRDBNet(num_in_ch=3,num_out_ch=3,num_feat=64,num_block=23,num_grow_ch=32,scale=4,)
    _model = RealESRGANer(scale=4,model_path=str(Model_PATH),model=model,tile=0,tile_pad=10,pre_pad=0,half=device.type == "cuda",device=device,)
    return _model
def upscale_image(image, scale):
    if scale not in (2,4):
        raise ValueError("Scale must be 2 or 4.")
    upscaper = get_upscaler()
    output, _ = upscaper.enhance(image, outscale=scale)
    return output
   
