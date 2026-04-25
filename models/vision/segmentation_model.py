import torch
import torchvision.transforms as T
from torchvision.models.segmentation import deeplabv3_resnet50
import cv2
import numpy as np
from PIL import Image

model = deeplabv3_resnet50(pretrained=True)
model.eval()

transform = T.Compose([
    T.Resize((512, 512)),
    T.ToTensor(),
])

def segment_pcb(image_path):

    img = Image.open(image_path).convert("RGB")
    tensor = transform(img).unsqueeze(0)

    with torch.no_grad():
        output = model(tensor)["out"][0]

    mask = output.argmax(0).byte().cpu().numpy()

    return (mask > 0).astype(np.uint8) * 255


def overlay_mask(image_path, mask):

    img = cv2.imread(image_path)
    mask_color = cv2.applyColorMap(mask, cv2.COLORMAP_JET)

    overlay = cv2.addWeighted(img, 0.7, mask_color, 0.3, 0)

    out_path = image_path + "_overlay.png"
    cv2.imwrite(out_path, overlay)

    return out_path
