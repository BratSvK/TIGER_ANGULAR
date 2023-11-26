import { Component, OnInit, TemplateRef } from '@angular/core';
import { faClock } from '@fortawesome/free-regular-svg-icons';
import { faSquarePollVertical } from '@fortawesome/free-solid-svg-icons';
import { BsModalService, BsModalRef } from 'ngx-bootstrap/modal';


@Component({
    selector: 'Detatction',
    templateUrl: './detection.component.html',
    styleUrls: ['./detection.component.scss']
})
export class DetectionComponent implements OnInit {
    clockIcon = faClock;
    resultIcon = faSquarePollVertical;
    modalRef: BsModalRef;

    constructor(private modalService: BsModalService) { }

    ngOnInit(): void {
        
    }

    public openModal(template: TemplateRef<any>){
        this.modalRef = this.modalService.show(template);
      }
}
