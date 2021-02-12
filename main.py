from keras.preprocessing import image
from keras.applications.imagenet_utils import preprocess_input

import numpy as np

def load_image(path:str):
    img = image.load_img(path, target_size=None)
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    return img, x

def load_img_dir():
    pass

path = "test_images/blockDiagram_2.jpg"

img, x = load_image(path)

print(type(img))
print(type(x))