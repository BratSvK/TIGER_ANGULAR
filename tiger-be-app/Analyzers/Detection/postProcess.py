import json

def read_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

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

def get_lymphocyte_count(json_data):
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

def main():
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

if __name__ == "__main__":
    main()
