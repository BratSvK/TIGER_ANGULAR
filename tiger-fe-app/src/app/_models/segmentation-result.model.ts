export enum SegmentationTypeAlgo {
    CMeans = 1,
    FuzzyCMeans = 2,
    ThresholdBased = 3
}

export interface SegmentationResult {
    segmentedOrigin: string | null;
    segmentedPrediction: string | null;
    dice: number;
}
