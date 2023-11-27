from flask import jsonify, request, Flask
from flask_cors import CORS
from PIL import Image  # Import knižnice Pillow

app = Flask(__name__)
app.config["DEBUG"] = True
CORS(app)
detection_api = 'api/detection'
tils_result = { 'tils': 88 }

@app.route(f"/{detection_api}/mock", methods=['GET'])
def runResult():
    return jsonify(tils_result)


@app.route(f"/{detection_api}/scan", methods=['POST'])
def runScan():
    # uploaded_file = request.files['file']
    # # Uloženie nahraného súboru
    # file_path = f"uploads/{uploaded_file.filename}"
    # uploaded_file.save(file_path)

    # Získanie veľkosti obrázka
    # with Image.open(file_path) as img:
    #     width, height = img.size

    # print(f"Veľkosť obrázka {uploaded_file.filename}: {width}x{height} pixelov")

    return jsonify(tils_result)

app.run()