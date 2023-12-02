import sys
import os

from PIL import Image

def process_image(path):
    try:
        img = Image.open(path)
        img = img.convert('RGB')
        pixels = img.load()
    except IOError as err:
        print('cannot open file' + err)
        sys.exit()

    tumor = (0, 255, 0)  # green
    stroma = (0, 0, 255)  # blue
    others = (255, 0, 0)  # red

    for i in range(0, img.width):
        for j in range(0, img.height):
            
            rgb_others = (120, 120, 120)
            rgb_tumor = (180, 180, 180)
            is_others = all(c1 <= c2 for c1, c2 in zip(pixels[i, j], rgb_others))
            is_tumor= all(c1 <= c2 for c1, c2 in zip(pixels[i, j], rgb_tumor))

            if is_others: 
                pixels[i, j] = others
            elif is_tumor:
                pixels[i, j] = tumor
            else:
                pixels[i, j] = stroma
    img.save(path)

# if __name__ == '__main__':

#     dir_cells_masks = "../../images" #cesta ku obrazkom, ktore bude rovno segmentovat (prefarbovat)

#     for filename in os.listdir(dir_cells_masks):
#         f = os.path.join(dir_cells_masks, filename)
#         if os.path.isfile(f):
#             process_image(f)
