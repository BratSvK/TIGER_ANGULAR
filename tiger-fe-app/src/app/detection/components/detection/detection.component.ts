import { Component, OnInit, TemplateRef } from '@angular/core';
import { faClock } from '@fortawesome/free-regular-svg-icons';
import { faSquarePollVertical } from '@fortawesome/free-solid-svg-icons';
import { BsModalService, BsModalRef } from 'ngx-bootstrap/modal';
import { Observable, catchError, map, of } from 'rxjs';
import { DetectionResult } from '../../../_models/detection-result.model';
import { DetectionService } from '../../services/detection.service';
import { SubSink } from 'subsink';
import { ToastrService } from 'ngx-toastr';

@Component({
    selector: 'Detatction',
    templateUrl: './detection.component.html',
    styleUrls: ['./detection.component.scss']
})
export class DetectionComponent implements OnInit {
    clockIcon = faClock;
    resultIcon = faSquarePollVertical;
    modalRef: BsModalRef;
    detectionResult: DetectionResult;
    mockResult: DetectionResult =  { tils: 0 };
    private subs = new SubSink();
    loading: boolean = false;

    constructor(
        private modalService: BsModalService, 
        private detectService: DetectionService,
        private toastr: ToastrService
    ) { }

    ngOnInit(): void {
        this.detectionResult = this.mockResult;
    }

    ngOnDestroy(): void {
        this.subs.unsubscribe();
      }
    

    public sentTissueForScan(file: File) {
        console.log("Obrázok bol poslaný na scanning: " + file.size);
        this.loading = true;
        this.subs.sink = this.detectService.getDetectionResult$(file).pipe(
            map((result: DetectionResult) => {
                this.toastr.success('Detekcia prebehla úspešne.');
                this.detectionResult = result;
                this.loading = false;
            }),
            catchError((error) => {
              this.toastr.error('Niečo sa pokailo, skúste neskôr');
              this.loading = false;
              return of(this.mockResult);
            })).subscribe();
    }

    public openModal(template: TemplateRef<any>) {
        this.modalRef = this.modalService.show(template);
    }
}
