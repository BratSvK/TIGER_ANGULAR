import { Component, ElementRef, Input } from '@angular/core';

@Component({
  selector: 'SegmentationResultImg',
  templateUrl: './segmentation-result-img.component.html',
  styleUrl: './segmentation-result-img.component.scss'
})
export class SegmentationResultImgComponent  {
  @Input() imageUrl: string;

  constructor() { }
}
