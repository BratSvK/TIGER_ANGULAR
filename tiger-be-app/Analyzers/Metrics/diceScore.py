import sys
import os
from PIL import Image

resize_val = 256

def get_dice_score(clustered_img_path, original_img_path, image_name):
    dice_score = 0
    f_clustered = os.path.join(clustered_img_path, image_name)
    f_original = os.path.join(original_img_path, image_name)
    try:
      clustered_img = Image.open(f_clustered)
      origin_img = Image.open(f_original)
      original_img = origin_img.resize((resize_val, resize_val))
      clustered_img = clustered_img.convert('RGB')
      original_img = original_img.convert('RGB')
      clustered_img_pixels = clustered_img.load()
      original_img_pixels = original_img.load()
    except IOError as err:
        print('cannot open file' + err)
        sys.exit()

    tumor = (0, 255, 0)  # green
    stroma = (0, 0, 255)  # blue

    all_counter_tumor = 0
    all_counter_stroma = 0
    match_stroma = 0
    match_tumor = 0

    for i in range(original_img.width):
      for j in range(original_img.height):
          if original_img_pixels[i, j] == stroma:
             all_counter_stroma += 1
          if clustered_img_pixels[i, j] == stroma:
             all_counter_stroma += 1
          if original_img_pixels[i, j] == tumor:
             all_counter_tumor += 1
          if clustered_img_pixels[i, j] == tumor:
             all_counter_tumor += 1
          if original_img_pixels[i, j] == stroma and clustered_img_pixels[i, j] == stroma:
             match_stroma += 1
          elif original_img_pixels[i, j] == tumor and clustered_img_pixels[i, j] == tumor:
             match_tumor += 1

    dice_score_stroma = 2 * match_stroma / all_counter_stroma if all_counter_stroma > 0 else 0
    dice_score_tumor = 2 * match_tumor / all_counter_tumor if all_counter_tumor > 0 else 0
    dice_score += (dice_score_stroma + dice_score_tumor) / 2

    print('final_dice_score', dice_score)

    return dice_score

if __name__ == '__main__':
    clustered_images_path = "../clustered_images-cells" #cesta ku segmentovanym obrazkom
   #  original_images_path = "./Mapovanie/roi-level-annotations-tissue-cells-masks-mapped" #cesta ku ground-truth obrazkom
   #  get_dice_score(clustered_images_path, original_images_path)