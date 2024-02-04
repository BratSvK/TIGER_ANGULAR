export enum SegmentationTypeAlgo {
    CMeans = 1,
    FuzzyCMeans = 2,
    ThresholdBased = 3,
    VGG16 = 4,
    UNET = 5
}

export enum CnnTypeAlgo {
    VGG16 = 1,
    Inception = 2
}

export interface SegmentationResult {
    segmentedOrigin: string | null;
    segmentedPrediction: string | null;
    dice: number;
}
