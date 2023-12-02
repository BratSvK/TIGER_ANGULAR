import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { BaseService } from '../../../services/base.service';
import { SEGMENTATION_API } from '../../constants/ApiRoutes';
import { SegmentationResult, SegmentationTypeAlgo } from '../../_models/segmentation-result.model';

@Injectable()
export class SegmentationService extends BaseService {

  constructor(http: HttpClient) {
    super(http) 
  }

  getSegmentedTissue$(file: File, typeAnalyzer: SegmentationTypeAlgo): Observable<SegmentationResult> {
    return this.sendFilesToAnalyzer<SegmentationResult>(file, SEGMENTATION_API, typeAnalyzer);
  }
}
