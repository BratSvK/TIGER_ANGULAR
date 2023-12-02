import sys
import numpy as np
import cv2 as cv
import json
import os
from PIL import Image

from Analyzers.Segmentation.kmeansFuzzy import color_image_to_segment



def k_Means(path, K):
    
    try:
        img = cv.imread(path) #treba spravne nastavit cestu podla toho kde mate ulozene obrazky
    except IOError as err:
        print('cannot open file' + err)
        sys.exit()

    if len(img.shape) < 3:
      Z = img.reshape((-1,1))
    elif len(img.shape) == 3:
      Z = img.reshape((-1,3))    

    Z = np.float32(Z)

    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    ret, label, center = cv.kmeans(Z, K, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)
    
    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    Clustered_Image = res.reshape((img.shape))
    clustered_img = Image.fromarray(Clustered_Image)
    clustered_img.save(path)
    color_image_to_segment(path, K);
    

def get_number_of_clusters(json_path):
    
    data = []
    dictionary = {}

    with open(json_path) as f:
      data = json.load(f)
    
    for key, value in data.items():
      number_of_clusters = 0
      for val in value:
          if val == True:
              number_of_clusters += 1

      dictionary[key] = number_of_clusters

    return dictionary

def create_clustered_images():
    
    folder_name = "../clustered_images-cells" #cesta kde sa maju ulozit vysledne obrazky po k-means
    json_path = 'Mapovanie/roi-level-annotations-tissue-cells-masks.json'

    if not os.path.exists(folder_name): 
      os.makedirs(folder_name)

    dict = get_number_of_clusters(json_path)

    for key in dict:
      Clusters = dict[key]
      Input_Image = cv.imread('../images-cells/{}'.format(key)) #treba spravne nastavit cestu podla toho kde mate ulozene obrazky
      Clustered_Image = k_Means(Input_Image, Clusters)
      output_path = os.path.join(folder_name, key)
      cv.imwrite(output_path, Clustered_Image)


if __name__ == '__main__':
    create_clustered_images()
