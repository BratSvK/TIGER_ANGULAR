import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { BaseService } from '../../../services/base.service';
import { DETECTION_API } from '../../constants/ApiRoutes';
import { DetectionResult } from '../../_models/detection-result.model';

@Injectable()
export class DetectionService extends BaseService {

  constructor(http: HttpClient) {
    super(http) 
  }

  getDetectionResult$(file: File): Observable<DetectionResult> {
    return this.sendFilesToAnalyzer(file, DETECTION_API);
  }
}
