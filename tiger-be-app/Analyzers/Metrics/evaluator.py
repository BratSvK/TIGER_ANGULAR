import sys
import os

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt


def get_dice_score(clustered_img_path, original_img_path):

    # Získanie zoznamu súborov v adresári usporiadaných vzostupne
    predicted_images = sorted(os.listdir(clustered_img_path), key=None)
    origin_images = sorted(os.listdir(original_img_path), key=None)

    if '.DS_Store' in predicted_images:
        predicted_images.remove('.DS_Store')

    dice_scores = np.zeros(len(origin_images))
    images_count = 0
    for clustered, original in zip(predicted_images, origin_images):
        f_clustered = os.path.join(clustered_img_path, clustered)
        f_original = os.path.join(original_img_path, original)
        try:
            clustered_img = Image.open(f_clustered)
            original_img = Image.open(f_original)
            clustered_img = clustered_img.convert('RGB')
            original_img = original_img.convert('RGB')
            original_img = original_img.resize((256, 256))
        except IOError as err:
            print('cannot open file' + err)
            sys.exit()

        # fig, axes = plt.subplots(1, 2)
        # axes[0].imshow(original_img)
        # axes[1].imshow(clustered_img)
        # plt.show()

        matrix = get_confuison_matrix(clustered_img, original_img)
        TP = matrix[ 0 , 0 ]
        FN = matrix[ 0 , 1 ]
        FP = matrix[ 1 , 0 ]
        dice = (2 * TP)/((2 * TP) + FP + FN)
        dice_scores[images_count] = dice
        images_count += 1


    average_dice = sum(dice_scores) / len(dice_scores)
    print("Priemerné Dice skóre:", average_dice)

def get_confuison_matrix(clustered_img, original_img):
    tumor = (0, 255, 0)  # green
    stroma = (0, 0, 255)  # blue
    # Initialize counters for confusion matrix
    true_tumor = 0
    true_stroma = 0
    false_tumor_as_stroma = 0
    false_stroma_as_tumor = 0

    # Get pixel data
    predicted_pixels = np.array(clustered_img)
    ground_truth_pixels = np.array(original_img)

    # fig, axes = plt.subplots(1, 2)
    # axes[0].imshow(predicted_pixels)
    # axes[1].imshow(ground_truth_pixels)
    # plt.show()

    predicted_flat = predicted_pixels.reshape(-1, 3)
    ground_truth_flat = ground_truth_pixels.reshape(-1, 3)
    # Calculate confusion matrix
    for pred_pixel, gt_pixel in zip(predicted_flat, ground_truth_flat):
        if np.array_equal(pred_pixel, tumor):  # Green for tumor
            if np.array_equal(gt_pixel, tumor):
                true_tumor += 1
            else:
                false_tumor_as_stroma += 1
        elif np.array_equal(pred_pixel, stroma):  # Blue for stroma
            if np.array_equal(gt_pixel, stroma):
                true_stroma += 1
            else:
                false_stroma_as_tumor += 1

    # Create confusion matrix
    confusion_matrix = np.array([[true_tumor, false_stroma_as_tumor],
                                 [false_tumor_as_stroma, true_stroma]])

    # Výpis confusion matrix
    # print(confusion_matrix)
    return confusion_matrix

if __name__ == '__main__':
    clustered_images_path = "fcm_images/"  # cesta ku segmentovanym obrazkom
    original_images_path = "masky_colored/roi-level-annotations-tissue-bcss-masks-mapped-nove"  # cesta ku ground-truth obrazkom

    get_dice_score(clustered_images_path, original_images_path)
    # get_confuison_matrix(clustered_images_path, original_images_path)