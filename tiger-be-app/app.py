from flask import jsonify, request, Flask
from flask_cors import CORS
import shutil
from Analyzers.Detection.tils_score import calculate_tils_score, process_image_origin, process_image_origin_pred, process_image_rectangle
from Analyzers.Segmentation.CNN.CNN_UNET.Rekonstrukcia import efficident_unet_segmentation

from Analyzers.Segmentation.CNN.CNN_VGG16.img_predictor import predict_multiple
from Analyzers.Segmentation.eAlgoTypes import SegmentationTypeAlgo
from Helpers.ImageHelper import ImageHelper
from Analyzers.Segmentation.treshold import process_image
from Analyzers.Metrics.diceScore import get_dice_score
from Analyzers.Segmentation.kmeans import k_Means
from Analyzers.Segmentation.kmeansFuzzy import FCM_INIT
from Models.DetectionResultDTO import DetectionResultDTO
from Models.SegmentationResultDTO import SegmentationResultDTO
from Analyzers.Detection.DetectionService import DetectionService, extract_lymphocyte_count, get_lymphocyte_count
import matplotlib.pyplot as plt
import time

app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)
detection_api = 'api/detection'
segmentation_api = 'api/segmentation'


# @app.route(f"/{detection_api}/mock", methods=['GET'])
# def runResult():
#     return jsonify(tils_result)


@app.route(f"/{detection_api}/scan", methods=['POST'])
def runDetection():
    start_time = time.time()
    # Uloženie nahraného súboru
    image_file = request.files['file']
    image_name = image_file.filename
    detection_path = f"detection/tils/{image_name}"
    detection_coco_path = f"detection/coco/{image_name}"
    origin_coco_path = f"detection/coco/tiger-coco.json"
    origin_path = f"detection/origin/{image_name}"
    square_path = f"detection/squares/{image_name}"
    image_file.save(origin_path)
    shutil.copy(origin_path, detection_path)
    shutil.copy(origin_path, square_path)
    efficident_unet_segmentation(detection_path)

    detection_service = DetectionService()
    detection_service.detect(origin_path, detection_coco_path)
    tils = calculate_tils_score(detection_path, detection_coco_path)
    process_image_origin_pred(square_path, f"{detection_coco_path}.json")
    process_image_origin(origin_path, origin_coco_path)

    origin_square_img = ImageHelper.LoadImageAndEncodeToBase64(origin_path)
    detection_img = ImageHelper.LoadImageAndEncodeToBase64(square_path)
    lymph_count = get_lymphocyte_count(f"{detection_coco_path}.json")

    end_time = time.time()
    execution_time = end_time - start_time

    response_data = DetectionResultDTO(
        detection_origin=origin_square_img,
        detection_prediction=detection_img,
        lym_count=lymph_count,
        tils=tils,
        execution_time=execution_time
    )

    return response_data.to_dict()


@app.route(f"/{segmentation_api}/scan", methods=['POST'])
def runSegmentation():
    # Uloženie nahraného súboru
    image_file = request.files['file']
    analyzer_value = int(request.form['analyzer'])
    type_analyzer = SegmentationTypeAlgo(analyzer_value)
    image_name = image_file.filename
    prediction_path = f"predictions/{image_name}"
    image_file.save(prediction_path)

    # Original truth image
    segmented_origin_path = f"origins_prediction/{image_name}"
    segmented_origin_image = ImageHelper.LoadImageAndEncodeToBase64(segmented_origin_path)
    
    # run segmentation algo
    if type_analyzer == SegmentationTypeAlgo.CMeans:
        cluster_numbers_predicted = predict_multiple(prediction_path)
        k_Means(prediction_path, cluster_numbers_predicted)
    elif type_analyzer == SegmentationTypeAlgo.FuzzyCMeans:
        cluster_numbers_predicted = predict_multiple(prediction_path)
        FCM_INIT(prediction_path, cluster_numbers_predicted, cluster_numbers_predicted + 1)
    elif type_analyzer == SegmentationTypeAlgo.ThresholdBased:
        process_image(prediction_path)
    elif type_analyzer == SegmentationTypeAlgo.UNET:
        efficident_unet_segmentation(prediction_path)
    else:
        print("Neznáma hodnota")

    segmented_prediction_image = ImageHelper.LoadImageAndEncodeToBase64(prediction_path)
    dice_value = round(get_dice_score('predictions', 'origins_prediction', image_name) * 100, 2)

    response_data = SegmentationResultDTO(
        segmented_origin=segmented_origin_image,
        segmented_prediction=segmented_prediction_image,
        dice=dice_value
    )

    return response_data.to_dict()


if __name__ == "__main__":
    app.run()
