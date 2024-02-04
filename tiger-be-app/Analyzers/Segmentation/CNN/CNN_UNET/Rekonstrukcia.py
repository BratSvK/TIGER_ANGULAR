from tensorflow import reshape, shape, reduce_sum, reduce_mean
import numpy as np
import cv2
from PIL import Image
import sys
from efficientunet import *
import cv2

base_dir = 'Analyzers/Segmentation/CNN/CNN_UNET/data'

def final_map(path):
    try:
        img = Image.open(path)
        img = img.convert('RGB')
        pixels = img.load()
    except IOError as err:
        print('cannot open file', err)
        sys.exit()

    for i in range(0, img.width):
        for j in range(0, img.height):
            if pixels[i, j] == (0, 255, 0):
                pixels[i, j] = (0, 0, 255)
            elif pixels[i, j] == (0, 0, 255):
                pixels[i, j] = (255, 0, 0)
            elif pixels[i, j] == (255, 0, 0):
                pixels[i, j] = (0, 255, 0)

    img.save(path)

def efficident_unet_segmentation(img_path):
    pocet_tried = 3
    model = get_efficient_unet_b0((512, 512, 3), out_channels=pocet_tried, pretrained=True)
    model.load_weights(f"{base_dir}/model_weights.h5")

    img = cv2.imread(img_path)
    test_img = cv2.resize(img, (512, 512))
    test_img = (test_img.astype('float32')) / 255.
    test_img_input = np.expand_dims(test_img, 0)
    prediction = model.predict(test_img_input)
    prediction = prediction[0, :, :, :]

    for i in range(prediction.shape[0]):
        for j in range(prediction.shape[1]):
            logits = np.array(prediction[i, j, :])
            probabilities = np.exp(logits) / np.sum(np.exp(logits))
            index_of_max_prob = np.argmax(probabilities)

            for p in range(3):
                probabilities[p] = 0

            probabilities[index_of_max_prob] = 255

            for k in range(prediction.shape[2]):
                prediction[i, j, k] = probabilities[k]

    cv2.imwrite(img_path, prediction.astype(np.uint8))
    final_map(img_path)
