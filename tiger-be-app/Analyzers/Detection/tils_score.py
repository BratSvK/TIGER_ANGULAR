import json
import sys
import os

from PIL import Image, ImageDraw

def process_images(image_dir, tiger_coco_json):
    with open(tiger_coco_json, 'r') as json_file:
        tiger_coco = json.load(json_file)

    for original_image in os.listdir(image_dir):
        index_id = next((i for i, image in enumerate(tiger_coco['images']) if image['file_name'] == original_image), None)
        annotations = [image for image in tiger_coco['annotations'] if image['image_id'] == image_id]
        if annotations:
            image_path = os.path.join(image_dir, original_image)
            draw_rectangle_on_image(image_path, annotations)


def draw_rectangle_on_origin(image_path, annotations):
    try:
        img = Image.open(image_path)
        img = img.convert('RGB')
    except IOError as err:
        print('cannot open file ', err)
        sys.exit()

    yellow = (255, 255, 0)
    draw = ImageDraw.Draw(img)
    for i, annotation in enumerate(annotations):
        bbox = annotation['bbox']
        x, y, width, height = bbox
        draw.rectangle([x, y, x + width, y + height], outline=yellow)
    img.save(image_path)

def draw_rectangle_on_origin_predictions(image_path, annotations):
    try:
        img = Image.open(image_path)
        img = img.convert('RGB')
    except IOError as err:
        print('cannot open file ', err)
        sys.exit()

    yellow = (255, 255, 0)
    draw = ImageDraw.Draw(img)
    for i, annotation in enumerate(annotations):
        bbox = annotation['bbox_pred']
        width = int(20)
        height = int(20)
        x, y = map(lambda v: abs(int(round(v))), bbox)
        draw.rectangle([x, y, x + width, y + height], outline=yellow)
    img.save(image_path)

def process_image_origin(image_path, tiger_coco_json):
    with open(tiger_coco_json, 'r') as json_file:
        tiger_coco = json.load(json_file)

    original_image = os.path.basename(image_path)
    index_id = next((i for i, image in enumerate(tiger_coco['images']) if image['file_name'] == original_image), None)
    image_id = tiger_coco['images'][index_id]['id']
    annotations = [image for image in tiger_coco['annotations'] if image['image_id'] == image_id]
    if annotations:
        draw_rectangle_on_origin(image_path, annotations)

def process_image_origin_pred(image_path, tiger_coco_json):
    with open(tiger_coco_json, 'r') as json_file:
        tiger_coco = json.load(json_file)

    original_image = os.path.basename(image_path)
    index_id = next((i for i, image in enumerate(tiger_coco['images']) if image['file_name'] == original_image), None)
    image_id = tiger_coco['images'][index_id]['id']
    annotations = [image for image in tiger_coco['annotations'] if image['image_id'] == image_id]
    if annotations:
        draw_rectangle_on_origin_predictions(image_path, annotations)

def process_image_rectangle(image_path, tiger_coco_json):
    with open(tiger_coco_json, 'r') as json_file:
        tiger_coco = json.load(json_file)

    original_image = os.path.basename(image_path)
    index_id = next((i for i, image in enumerate(tiger_coco['images']) if image['file_name'] == original_image), None)
    image_id = tiger_coco['images'][index_id]['id']
    annotations = [image for image in tiger_coco['annotations'] if image['image_id'] == image_id]
    if annotations:
        draw_rectangle_on_image(image_path, annotations)

def draw_rectangle_on_image(image_path, annotations):
    try:
        img = Image.open(image_path)
        img = img.convert('RGB')
        pixels = img.load()
    except IOError as err:
        print('cannot open file ', err)
        sys.exit()
    yellow = (255, 255, 0)
    stroma = (0, 0, 255)
    draw = ImageDraw.Draw(img)
    for i, annotation in enumerate(annotations):
        bbox = annotation['bbox_pred']
        width = int(20)
        height = int(20)
        x, y = map(lambda v: abs(int(round(v))), bbox)
        for j in range(x, x + width):
            for k in range(y, y + height):
                if (j < img.width and k < img.height):
                    if pixels[j, k] == stroma:
                        draw.rectangle([x, y, x + width, y + height], fill=yellow, outline=yellow)
    img.save(image_path)

def calculate_area(image_path):
    lymphocytes_area = 0
    stroma_area = 0
    yellow = (255, 255, 0)
    blue = (0, 0, 255)
    try:
        img = Image.open(image_path)
        img = img.convert('RGB')
        pixels = img.load()
    except IOError as err:
        print('cannot open file ', err)
        sys.exit()
    for i in range(0, img.width):
        for j in range(0, img.height):
            if pixels[i, j] == yellow:
                lymphocytes_area += 1
            if pixels[i, j] == blue:
                stroma_area += 1
    tils_score = round(100 * (lymphocytes_area / stroma_area), 2)
    image_name = image_path.split('/')[1]
    print(f'Tils score pre obrázok "{image_name}" je: {tils_score}%')

    return tils_score

def calculate_tils_score(segmented_path, detection_path):
    json_path = f"{detection_path}.json"
    process_image_rectangle(segmented_path, json_path)
    return calculate_area(segmented_path)