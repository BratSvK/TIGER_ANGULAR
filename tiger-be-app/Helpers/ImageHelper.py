import base64
import io

class ImageHelper:
    @staticmethod
    def LoadImageAndEncodeToBase64(file_path):
        with open(file_path, 'rb') as image_file_binary:
            image_base64  = base64.b64encode(image_file_binary.read()).decode('utf-8')
            image_data = f'data:image/png;base64,{image_base64}';

        return image_data
    

    @staticmethod
    def LoadImageFromPath(file_path):
        with open(file_path, 'rb') as image_file_binary:
            image_data = io.BytesIO(image_file_binary)

        return image_data