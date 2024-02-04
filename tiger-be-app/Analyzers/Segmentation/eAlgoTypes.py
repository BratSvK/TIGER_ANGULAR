from enum import Enum


class SegmentationTypeAlgo(Enum):
    CMeans = 1
    FuzzyCMeans = 2
    ThresholdBased = 3
    VGG16 = 4,
    UNET = 5
