export interface DetectionResult {
    detectionOrigin: string | null;
    detectionPrediction: string | null;
    tils: number;
    lymCount: number;
    executionTime: number;
}