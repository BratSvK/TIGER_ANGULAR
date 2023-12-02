import { Component, OnDestroy, OnInit } from '@angular/core';
import { Algorithm } from '../../../_models/segmentation-selection.model';
import { SegmentationResult, SegmentationTypeAlgo } from '../../../_models/segmentation-result.model';
import { SegmentationService } from '../../services/segmentation.service';
import { catchError, map, of, tap } from 'rxjs';
import { ToastrService } from 'ngx-toastr';
import { SubSink } from 'subsink';

@Component({
    selector: 'Segmentation',
    templateUrl: './segmentation.component.html',
    styleUrls: ['./segmentation.component.scss']
})
export class SegmentationComponent implements OnInit, OnDestroy  {
    private subs = new SubSink();
    loading: boolean = false;
    selectedAlgoritm: Algorithm;
    segmentationAlgorithms: Algorithm[] = [
        new Algorithm(SegmentationTypeAlgo.CMeans, 'C-Means'),
        new Algorithm(SegmentationTypeAlgo.FuzzyCMeans, 'Fuzzy C-Means'),
        new Algorithm(SegmentationTypeAlgo.ThresholdBased, 'Threshold-Based')
    ];
    segmentedResult: SegmentationResult;

    constructor(
        private segmentService: SegmentationService, 
        private toastr: ToastrService
    ) {}
  

    ngOnDestroy(): void {
       this.subs.unsubscribe();
    }

    ngOnInit(): void {
        this.segmentedResult = {
            segmentedOrigin: null,
            segmentedPrediction: null,
            dice: 0
          };
    }

    onSegmentationStart(file: File) {
        console.log("Obrázok bol poslaný na segmentáciu: " + file.size);
        this.loading = true;
        this.subs.sink = this.segmentService.getSegmentedTissue$(file, this.selectedAlgoritm.id).pipe(
            map((result: SegmentationResult) => {
                this.toastr.success('Segmentácia prebehla úspešne.');
                this.segmentedResult = result;
                this.loading = false;
            }),
            catchError((error) => {
              this.toastr.error('Niečo sa pokailo, skúste neskôr');
              this.loading = false;

              return of(error);
            })).subscribe();
    }
}
