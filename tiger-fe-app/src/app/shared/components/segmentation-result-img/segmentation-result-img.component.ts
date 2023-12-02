import { Component, Input, OnChanges, OnInit, SimpleChanges } from '@angular/core';

@Component({
  selector: 'SegmentationResultImg',
  templateUrl: './segmentation-result-img.component.html',
  styleUrl: './segmentation-result-img.component.scss'
})
export class SegmentationResultImgComponent implements OnInit {
  @Input() imageBase64: string | null;

  constructor() { }

  ngOnInit(): void {
    // this.loadImageUrl();
  }
  
}
