import { Component, OnInit } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { Algorithm } from '../../../_models/segmentation-selection.model';

@Component({
    selector: 'Segmentation',
    templateUrl: './segmentation.component.html',
    styleUrls: ['./segmentation.component.scss']
})
export class SegmentationComponent implements OnInit {
    loading: boolean = false;
    selectedAlgoritm: Algorithm;
    segmentationAlgorithms: Algorithm[] = [
        new Algorithm(1, 'C-Means'),
        new Algorithm(2, 'Threshold-Based'),
        new Algorithm(3, 'Fuzzy C-Means')
    ];

    public imageUrl1: string = 'url(../../../../assets/mock-segmentation-after.png)';
    public imageUrl2: string = 'url(../../../../assets/mock-segmentation-origin.png)';

    ngOnInit(): void {
    }


    onSelectAlgorithm() {
        console.log(this.selectedAlgoritm.name);
    }

    public onSegmentationStart(file: File) {
        console.log("Obrázok bol poslaný na segmentáciu: " + file.size);
        this.loading = true;
    }
}
