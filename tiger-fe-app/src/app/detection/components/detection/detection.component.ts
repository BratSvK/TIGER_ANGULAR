import { Component, OnInit, TemplateRef } from '@angular/core';
import { faClock } from '@fortawesome/free-regular-svg-icons';
import { faGraduationCap, faSquarePollVertical } from '@fortawesome/free-solid-svg-icons';
import { BsModalService, BsModalRef } from 'ngx-bootstrap/modal';
import { catchError, map, of } from 'rxjs';
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
    studyIcon = faGraduationCap;
    modalRef: BsModalRef;
    detectionResult: DetectionResult;
    mockResult: DetectionResult =  { tils: 0, detectionOrigin: null, detectionPrediction: null, lymCount: 0, executionTime: 0 };
    private subs = new SubSink();
    loading: boolean = false;
    default_img: string = '../../../../assets/waiting_image.png';
    default_tils: string = '../../../../assets/tils_info.png';

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
    
    doctorAdvanceMessage() {
        if (this.detectionResult.tils > 0 && this.detectionResult.tils <= 10) {
            return 'Nádor so žiadnymi / minimálnymi imunitnými bunkami';
        } else if (this.detectionResult.tils > 10 && this.detectionResult.tils <= 40) {
            return 'Nádor so stredným / heterogénnym infiltrátom';
        } else if (this.detectionResult.tils > 40 && this.detectionResult.tils <= 90) {
            return 'Nádor s vysokým imunitným infiltrátom';
        } else {
            return 'Čaká sa na výsledok...';
        }
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
