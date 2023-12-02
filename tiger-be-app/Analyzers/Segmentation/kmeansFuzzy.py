# Uprava obrazka
import os

import numpy as np
import cv2 as cv
import sys
import matplotlib.pyplot as plt
import skfuzzy as fuzz
from PIL import Image
import json

resize_val = 256
# Nadchádzajúca implementácia v Pythone je vyvinutá z otvoreného zdrojového kódu matlabovej implementácie BCET
def BalanceContrastEnhancementTechnique(gray_image):
    # normalizacia pixelov medzi 0 a 1
    obrazok_in = normalizacia_img_double(gray_image)
    l = np.min(obrazok_in.ravel())                      # pixel jas min
    h = np.max(obrazok_in.ravel())                      # pixel jas max
    e = np.mean(obrazok_in)                             # pixel jas priemer
    s = np.mean(pow(obrazok_in, 2))                     # rozptyl pixelov
    L = 0                                               # MINIMUM očakavany obrázok
    H = 255                                             # MAXIMUM
    E = 85                                              # MEAN  > 80 (Odporucane)

    # rovnice BCET
    b_menovatel = pow(h, 2) * (E - L) - s * (H - L) + pow(l, 2) * (H - E)
    b_citatel = 2 * (h * (E - L) - e * (H - L) + l * (H - E))

    b = b_menovatel / b_citatel
    a = (H - L) / ((h - l) * (h + l - 2 * b))
    c = L - a * pow((l - b), 2)

    y = a * pow((obrazok_in - b), 2) + c                # PARABOLICKA FUNCKIA
    # kedže pixel = 0-255 všetky prvky v poli prevedieme na také čisla
    y = y.astype(np.uint8)

    return y

def normalizacia_img_double(im):
    # pretranformovanie pola do jedneho riadku najdeme min a max a normalizujeme od 0-1
    min_val = np.min(im.ravel())
    max_val = np.max(im.ravel())
    out = (im.astype('float') - min_val) / (max_val - min_val)

    return out

def change_color_fuzzycmeans(cluster_membership, clusters):
 img = []
 for pix in cluster_membership.T:
     img.append(clusters[np.argmax(pix)])

 return img

def FCM(img_bcet, c, m):
    list_img = []
    img = cv.imread(f"bcet_images/{str(img_bcet)}")
    # transposed RGB image array, with the width and height swapped. rgb_img.T
    rgb_img = img.reshape((img.shape[0] * img.shape[1], 3))
    list_img.append(rgb_img)
    clusters = [c]

    for index, rgb_img in enumerate(list_img):
        img = np.reshape(rgb_img, (resize_val, resize_val, 3)).astype(np.uint8)
        shape = np.shape(img)
        for i, cluster in enumerate(clusters):
            center, u, u0, d, jm, p, fpc = fuzz.cluster.cmeans(
                rgb_img.T, cluster, m, error=0.005, maxiter=5000, init=None, seed=42)

            novy_obrazok = change_color_fuzzycmeans(u, center)
            fuzzy_obrazok = np.reshape(novy_obrazok, shape).astype(np.uint8)
            seg_img_1d = fuzzy_obrazok[:, :, 1]

            return seg_img_1d

def color_image_to_segment(path, c):
    try:
        # img_name = path.split("/")[-1]
        # print(img_name)
        img = Image.open(path)
        img = img.convert('RGB')
        pixels = img.load()

        # fig, axes = plt.subplots(1, 2)
        # axes[0].imshow(img)
        # axes[1].imshow(img)
        # plt.show()

        # Vytvorenie množiny pre jedinečné hodnoty RGB
        unique_rgb_values = set()

        # Prechádzanie pixelov a získanie jedinečných hodnôt RGB
        for y in range(img.height):
            for x in range(img.width):
                r, g, b = pixels[x, y]
                unique_rgb_values.add((r, g, b))

    except IOError as err:
        print('cannot open file' + err)
        sys.exit()

    unique_rgb_array = list(sorted(unique_rgb_values))[:c]
    if c == 3:
        (tumor_pix, stroma_pix, _) = unique_rgb_array
    else:
        (tumor_pix, stroma_pix) = unique_rgb_array

    tumor = (0, 255, 0)  # green
    stroma = (0, 0, 255)  # blue
    others = (255, 0, 0)  # red

    for i in range(0, img.width):
        for j in range(0, img.height):

            if pixels[i, j] == tumor_pix:  # invasive tumor
                pixels[i, j] = tumor

            elif pixels[i, j] == stroma_pix:  # tumor-associated stroma
                pixels[i, j] = stroma

            else:  # rest
                pixels[i, j] = others

    # plt.imshow(img)
    # plt.show()
    img.save(path)


def FCM_INIT(path, c, m):
    # nacitanie obrazka a uprava do 256 px a grayscale
    
    image1 = cv.imread(path)
    image1 = cv.resize(image1, (resize_val, resize_val), interpolation = cv.INTER_AREA)
    image = cv.cvtColor(image1, cv.COLOR_BGR2GRAY)
    
    # odstránenie šumu z obrazu pomocou medianBlur z knižnice openCV
    img_median = cv.medianBlur(image, 5)
    image_bcet = BalanceContrastEnhancementTechnique(img_median)
    cv.imwrite('bcet_images/img_bcet.jpg', image_bcet)
    image_FCM = FCM('img_bcet.jpg', c = c, m = m)
    cv.imwrite(path, image_FCM)
    color_image_to_segment(path, c)

if __name__ == '__main__':
    # nacitanie obrazka a uprava do 256 px a grayscale
    resize_val = 256

    # nacitanie obrazka do pamate v podobe intenzity pixelov
    # extrakcia obrysov
    k = 0
    folder_path = "raw_images/roi-level-annotations-tissue-bcss"
    cluster_path = "raw_images/roi-level-annotations-tissue-bcss-masks.json"

    # Open the file and load its contents as JSON
    with open(cluster_path, 'r') as file:
        json_data = json.load(file)

    for image_name in os.listdir(folder_path):
        image1 = cv.imread(f'{folder_path}/{image_name}')
        image1 = cv.resize(image1, (resize_val, resize_val), interpolation = cv.INTER_AREA)
        image = cv.cvtColor(image1, cv.COLOR_BGR2GRAY)
        # plt.imshow(image)
        # plt.show()



        if image_name in json_data:
            k = sum(json_data[image_name])
            print(f"Number of true booleans for {image_name}: {k}")
        else:
            print(f"No object found with the name {image_name}")


        # odstránenie šumu z obrazu pomocou medianBlur z knižnice openCV
        img_median = cv.medianBlur(image, 5)
        # plt.imshow(img_median)
        # plt.show()
        #
        # # BCET zvyšenie kontrastu obrázka
        image_bcet = BalanceContrastEnhancementTechnique(img_median)
        cv.imwrite('bcet_images/img_bcet.jpg', image_bcet)
        #
        # Získanie farieb pre jednotlivé clustre
        # farby = ['lime', 'blue', 'red']
        # Vytvorenie farebného mapovania (colormap)
        # cmap = plt.cm.colors.ListedColormap(farby)
        # #FCM segmentation for normal region of brain
        image_FCM = FCM('img_bcet.jpg', c = k, m = 4)
        cv.imwrite(f'fcm_images/{image_name}', image_FCM)
        # plt.imshow(image_FCM, cmap = cmap)
        # Zobrazenie farebných legend pre jednotlivé clustre
        # plt.colorbar(ticks=[0, 1, 2], label="Segmenty")
        # plt.show()

        color_image_to_segment(f'fcm_images/{image_name}', k)








