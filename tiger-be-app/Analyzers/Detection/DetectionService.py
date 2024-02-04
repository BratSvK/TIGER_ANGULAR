from keras.models import load_model
import numpy as np
import keras.utils as image
from keras.models import load_model
import json

base_dir_detection = 'Analyzers/Detection/trained_models/u_net/'
data_lymphocyte = 'Analyzers/Detection/selected_data.json'

class DetectionService:
    def __init__(self):
         self.smodel = load_model(f"{base_dir_detection}/Unet_Classifier.h5")
         
    def detect(self, input_img_path, coco_path):
        img = image.load_img(input_img_path, target_size=(256, 256))
        img = np.asarray(img)
        #plt.imshow(img)
        #plt.show()
        img = np.expand_dims(img, axis=0)
        img = img / 255.0  # Normalize pixel values to [0, 1]
        coords_pred = self.smodel.predict(img)
        save_predictions_to_json(coords_pred, coco_path)

    def extract_lymphocyte_count(json_data):
        annotations = json_data.get('annotations', [])

        data_list = []

        for annotation in annotations:
            count = annotation.get('bbox', [])
            image_id = annotation.get('image_id', None)

            data_list.append({
                'image_id': image_id,
                'lymphocyte_count': count
            })

        return data_list
    

def postprocess(detection_result):
            # Input file paths
        lymphocyte_file_path = "tmp.json"
        coordinates_file_path = "b16pati100dense512maskDefaultep5000LR001.json"

        # Read JSON files
        lymphocyte_data = read_json(lymphocyte_file_path)
        coordinates_data = read_json(coordinates_file_path)

        # Extract data
        lymphocyte_count = extract_lymphocyte_count(lymphocyte_data)
        coordinates = extract_coordinates(coordinates_data)

        modified_coordinates = modify_coordinates(lymphocyte_count, coordinates)

        # Display the extracted data
        print(f"Lymphocyte Count: {lymphocyte_count}")
        print(f"Coordinates: {coordinates}")

        output_file_path = "modified_output7.json"
        with open(output_file_path, 'w') as output_file:
            json.dump(modified_coordinates, output_file, indent=2)
        pass

def modify_coordinates(lymphocyte_count, coordinates):
    modified_coordinates = []

    for count in lymphocyte_count:
        for coord in coordinates:
            if (count['image_id'] == coord['image_id']):
                modified_coords = []
                index = 0
                for c in coord['bbox']:
                    if index > (count['lymphocyte_count']*2)-1:
                        break
                    modified_coords.append(c)
                    index = index + 1

                modified_coordinates.append({
                        'image_id': coord['image_id'],
                        'modified_coordinates': modified_coords
                    })

    return modified_coordinates

def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def extract_lymphocyte_count(json_path):
    json_data = read_json(json_path)
    annotations = json_data.get('annotations', [])

    data_list = []

    for annotation in annotations:
        count = annotation.get('bbox_pred', [])
        image_id = annotation.get('image_id', None)

        data_list.append({
            'image_id': image_id,
            'lymphocyte_count': count
        })

    return data_list

def get_lymphocyte_count(json_path):
    json_data = read_json(json_path)
    annotations = json_data.get('annotations', [])
    count = 0
    for annotation in annotations:
        count = count + 1

    return count

def extract_coordinates(json_data):
    annotations = json_data.get('annotations', [])

    data_list = []

    for annotation in annotations:
        bbox = annotation.get('bbox_pred', [])
        image_id = annotation.get('image_id', None)

        data_list.append({
            'image_id': image_id,
            'bbox': bbox
        })

    return data_list

def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_predictions_to_json(coords_pred, file_name):
    data = load_json(data_lymphocyte)
    predictions = {
        "info": {},
        "images": [],
        "annotations": []
    }

    for i, (coord_pred, image_info) in enumerate(zip(coords_pred, data['images'])):
        original_width = image_info['width']
        original_height = image_info['height']

        x_pred_original = (np.array(coord_pred[:len(coord_pred) // 2]) * original_width / 256).tolist()
        y_pred_original = (np.array(coord_pred[len(coord_pred) // 2:]) * original_height / 256).tolist()
        img_name = file_name.split('/')[2]
        prediction_entry = {
            "id": image_info['id'],
            "file_name": img_name,
            "height": original_height,
            "width": original_width
        }
        predictions["images"].append(prediction_entry)

        for j in range(len(x_pred_original)):
            annotation_entry = {
                "id": i * len(x_pred_original) + j,
                "category_id": 1,
                "iscrowd": 0,
                "image_id": image_info['id'],
                "area": 256.0,
                "bbox_pred": [x_pred_original[j], y_pred_original[j]]
            }
            predictions["annotations"].append(annotation_entry)

    json_file_path = f"{file_name}.json"
    with open(json_file_path, 'w') as json_file:
        json.dump(predictions, json_file, indent=4)