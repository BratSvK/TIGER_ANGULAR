import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';

@Component({
    selector: 'Segmentation',
    templateUrl: './segmentation.component.html',
    styleUrls: ['./segmentation.component.scss']
})
export class SegmentationComponent implements OnInit {

    constructor(
        private fb: FormBuilder,
    ) { }

    ngOnInit(): void {
        
    }
}
