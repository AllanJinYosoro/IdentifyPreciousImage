from dataset.cifar import pixelCal
from torchvision import transforms
from PIL import Image
import numpy as np

image_path = './data/train/labeled/0.jpg'
image = Image.open(image_path)
image_array = np.array(image)
channel1= np.average(image_array, axis=(0, 1))


image_path = './data/train/labeled/1.jpg'
image = Image.open(image_path)
image_array = np.array(image)
channel2= np.average(image_array, axis=(0, 1))
channel = np.vstack([channel1,channel2]).T

print(pixelCal())