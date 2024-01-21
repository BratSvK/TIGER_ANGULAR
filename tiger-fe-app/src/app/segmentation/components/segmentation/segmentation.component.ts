import { Component, OnDestroy, OnInit } from '@angular/core';
import { Algorithm } from '../../../_models/segmentation-selection.model';
import { CnnTypeAlgo, SegmentationResult, SegmentationTypeAlgo } from '../../../_models/segmentation-result.model';
import { SegmentationService } from '../../services/segmentation.service';
import { catchError, interval, map, of, takeWhile, tap } from 'rxjs';
import { ToastrService } from 'ngx-toastr';
import { SubSink } from 'subsink';
import { faCircleQuestion } from '@fortawesome/free-solid-svg-icons';

@Component({
    selector: 'Segmentation',
    templateUrl: './segmentation.component.html',
    styleUrls: ['./segmentation.component.scss']
})
export class SegmentationComponent implements OnInit, OnDestroy  {
    private subs = new SubSink();

    segmentationAlgorithms: Algorithm[] = [
        new Algorithm(SegmentationTypeAlgo.CMeans, 'C-Means'),
        new Algorithm(SegmentationTypeAlgo.FuzzyCMeans, 'Fuzzy C-Means'),
        new Algorithm(SegmentationTypeAlgo.ThresholdBased, 'Threshold-Based')
    ];
    cnnAlgorithms: Algorithm[] = [
        new Algorithm(CnnTypeAlgo.VGG16, 'VGG16'),
        new Algorithm(CnnTypeAlgo.Inception, 'Inception')
    ];

    infoIcon = faCircleQuestion;
    progressValue: number = 0;
    loading: boolean = false;
    selectedAlgoritm: Algorithm = this.segmentationAlgorithms[2];
    selectedCnnAlgoritm: Algorithm;
    segmentedResult: SegmentationResult;
    tooltipText: string = 
        `Máte na výber tri algoritmy: <br> <b>C-Means</b>, <b>Fuzzy C-Means</b> a <b>Threshold-Based </b>.
         <br>Pri prvých dvoch je potrebné definovať počet zhlukov <b>'K'</b>.`;

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
        this.progressValue = 30;
        const timer$ = interval(1000)
        .pipe(
            tap(() => this.progressValue += 10),
            takeWhile(() => this.progressValue <= 100)
        ).subscribe();

        this.loading = true;
        this.subs.sink = this.segmentService.getSegmentedTissue$(file, this.selectedAlgoritm.id)
        .pipe(
            map((result: SegmentationResult) => {
                timer$.unsubscribe(); // stop the timer
                this.toastr.success('Segmentácia prebehla úspešne.');
                this.segmentedResult = result;
                this.loading = false;
                this.progressValue = 100;
            }),
            catchError((error) => {
              timer$.unsubscribe(); // stop the timer
              this.toastr.error('Niečo sa pokailo, skúste neskôr');
              this.loading = false;

              return of(error);
            })).subscribe();
    }

    isCnnRequiredForPick(): boolean {
        if (!this.selectedAlgoritm) {
            return true;
          }
        
          switch (this.selectedAlgoritm.id) {
            case SegmentationTypeAlgo.CMeans:
            case SegmentationTypeAlgo.FuzzyCMeans:
              return false;
            default:
              return true;
          }
      }
}
