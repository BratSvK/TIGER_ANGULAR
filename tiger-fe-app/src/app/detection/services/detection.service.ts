import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { BaseService } from '../../../services/base.service';
import { DETECTION_API } from '../../constants/ApiRoutes';
import { DetectionResult } from '../../_models/personal-record.model';

@Injectable()
export class DetectionService extends BaseService {
  mockResult: DetectionResult =  { tils: 55 };

  constructor(http: HttpClient) {
    super(http) 
  }

  getDetectionResult$(file: File): Observable<DetectionResult> {
    const formData = new FormData();
    formData.append('file', file);
    return this.http.post<DetectionResult>(this.baseUrl + `${DETECTION_API}/scan`, formData);
  }
}
