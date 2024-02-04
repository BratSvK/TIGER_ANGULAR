class DetectionResultDTO:
    def __init__(self, detection_origin, detection_prediction, tils, lym_count, execution_time):
        self.detection_origin = detection_origin
        self.detection_prediction = detection_prediction
        self.tils = tils
        self.lym_count = lym_count
        self.execution_time = execution_time


    def to_dict(self):
        return {
            'detectionOrigin': self.detection_origin,
            'detectionPrediction': self.detection_prediction,
            'tils': self.tils,
            'lymCount': self.lym_count,
            'executionTime': self.execution_time
        }