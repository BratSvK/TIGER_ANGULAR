import { HttpClient } from '@angular/common/http';
import { Directive } from '@angular/core';
import { environment } from '../environments/environment';
import { Observable } from 'rxjs';
import { SegmentationTypeAlgo } from '../app/_models/segmentation-result.model';

@Directive()
export abstract class BaseService {
  baseUrl = environment.apiUrl;

  constructor(public http: HttpClient) { }


  sendFilesToAnalyzer<TResult>(file: File, typeOfAnalyzer: string, typeAlgo: SegmentationTypeAlgo = SegmentationTypeAlgo.CMeans): Observable<TResult> {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('analyzer', typeAlgo.toString());
    
    return this.http.post<TResult>(this.baseUrl + `${typeOfAnalyzer}/scan`, formData);
  }
}
