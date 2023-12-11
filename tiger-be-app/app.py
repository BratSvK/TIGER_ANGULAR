from flask import jsonify, request, Flask
from flask_cors import CORS

from Analyzers.Segmentation.CNN.CNN_VGG16.img_predictor import predict_multiple
from Analyzers.Segmentation.eAlgoTypes import SegmentationTypeAlgo
from Helpers.ImageHelper import ImageHelper
from Analyzers.Segmentation.treshold import process_image
from Analyzers.Metrics.diceScore import get_dice_score
from Analyzers.Segmentation.kmeans import k_Means
from Analyzers.Segmentation.kmeansFuzzy import FCM_INIT
from Models.SegmentationResultDTO import SegmentationResultDTO

app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)
detection_api = 'api/detection'
segmentation_api = 'api/segmentation'
tils_result = {'tils': 88}


@app.route(f"/{detection_api}/mock", methods=['GET'])
def runResult():
    return jsonify(tils_result)


@app.route(f"/{detection_api}/scan", methods=['POST'])
def runDetection():
    # uploaded_file = request.files['file']
    # # Uloženie nahraného súboru
    # file_path = f"uploads/{uploaded_file.filename}"
    # uploaded_file.save(file_path)

    # Získanie veľkosti obrázka
    # with Image.open(file_path) as img:
    #     width, height = img.size

    # print(f"Veľkosť obrázka {uploaded_file.filename}: {width}x{height} pixelov")

    return jsonify(tils_result)


@app.route(f"/{segmentation_api}/scan", methods=['POST'])
def runSegmentation():
    # Uloženie nahraného súboru
    image_file = request.files['file']
    analyzer_value = int(request.form['analyzer'])
    type_analyzer = SegmentationTypeAlgo(analyzer_value)

    prediction_path = f"predictions/{image_file.filename}"
    image_file.save(prediction_path)

    # Spustenie segmentácie s obrázkom podľa typu algoritmu

    segmented_origin_path = 'mock_images/mock-segmentation-origin.png'
    segmented_origin_image = ImageHelper.LoadImageAndEncodeToBase64(segmented_origin_path)
    cluster_numbers_predicted = predict_multiple(prediction_path);
    print(f"Predicted cluster: {cluster_numbers_predicted}")
    # run segmentation algo
    if type_analyzer == SegmentationTypeAlgo.CMeans:
        k_Means(prediction_path, cluster_numbers_predicted)
    elif type_analyzer == SegmentationTypeAlgo.FuzzyCMeans:
        FCM_INIT(prediction_path, cluster_numbers_predicted, cluster_numbers_predicted + 1)
    elif type_analyzer == SegmentationTypeAlgo.ThresholdBased:
        process_image(prediction_path)
    elif type_analyzer == SegmentationTypeAlgo.VGG16:
        predict_multiple(prediction_path)
    else:
        print("Neznáma hodnota")

    segmented_prediction_image = ImageHelper.LoadImageAndEncodeToBase64(prediction_path)
    dice_value = round(get_dice_score('predictions', 'mock_images'), 2) * 100

    response_data = SegmentationResultDTO(
        segmented_origin=segmented_origin_image,
        segmented_prediction=segmented_prediction_image,
        dice=dice_value
    )

    return response_data.to_dict();


if __name__ == "__main__":
    app.run()
