import { HttpClient } from '@angular/common/http';
import { Directive } from '@angular/core';
import { environment } from '../environments/environment';

@Directive()
export abstract class BaseService {
  baseUrl = environment.apiUrl;

  constructor(public http: HttpClient) { }
}
