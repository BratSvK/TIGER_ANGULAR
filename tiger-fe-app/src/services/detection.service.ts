import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { BaseService } from './base.service';
import { DETECTION_API } from '../app/constants/ApiRoutes';
import { DetectionResult } from '../app/_models/personal-record.model';

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

  getDetectionResult2$(file: File): Observable<DetectionResult> {
    return this.http.get<DetectionResult>(this.baseUrl + `${DETECTION_API}/mock`);
  }

  getDetectionResultMock$(file: File): Observable<DetectionResult> {
    return of(this.mockResult);
  }
}
