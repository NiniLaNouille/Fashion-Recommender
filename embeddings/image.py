from transformers import CLIPProcessor, CLIPModel
from PIL import Image
import requests

model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


def embed(image_url):

    image = Image.open(requests.get(image_url, stream=True).raw)

    inputs = processor(images=image, return_tensors="pt")

    outputs = model.get_image_features(**inputs)

    return outputs.detach().numpy()[0]
