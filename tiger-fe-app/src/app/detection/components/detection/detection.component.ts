import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';

@Component({
    selector: 'app-login',
    templateUrl: './detection.component.html',
    styleUrls: ['./detection.component.scss']
})
export class DetectionComponent implements OnInit {

    constructor(
        private fb: FormBuilder,
    ) { }

    ngOnInit(): void {
        
    }
}
