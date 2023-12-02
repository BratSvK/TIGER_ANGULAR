class SegmentationResultDTO:
    def __init__(self, segmented_origin, segmented_prediction, dice):
        self.segmented_origin = segmented_origin
        self.segmented_prediction = segmented_prediction
        self.dice = dice


    def to_dict(self):
        return {
            'segmentedOrigin': self.segmented_origin,
            'segmentedPrediction': self.segmented_prediction,
            'dice': self.dice
        }