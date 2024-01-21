import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TigerRoutingModule } from './tiger-routing.module';
import { TigerComponent } from './component/tiger/tiger.component';
import { DetectionComponent } from '../detection/components/detection/detection.component';
import { SegmentationComponent } from '../segmentation/components/segmentation/segmentation.component';
import { NavbarComponent } from './component/navbar/navbar.component';
import { ImageUploaderComponent } from '../shared/components/image-uploader/image-uploader.component';
import { FontAwesomeModule } from '@fortawesome/angular-fontawesome';
import { ModalModule } from 'ngx-bootstrap/modal';
import { DetectionService } from '../detection/services/detection.service';
import { FormsModule } from '@angular/forms';
import { ConnectProcessComponent } from '../shared/components/connect-process/connect-process.component';
import { SegmentationResultImgComponent } from '../shared/components/segmentation-result-img/segmentation-result-img.component';
import { SegmentationService } from '../segmentation/services/segmentation.service';
import { ProgressbarModule } from 'ngx-bootstrap/progressbar';
import { TooltipModule } from 'ngx-bootstrap/tooltip';

@NgModule({
  declarations: [
    TigerComponent,
    DetectionComponent,
    SegmentationComponent,
    NavbarComponent,
    ImageUploaderComponent,
    ConnectProcessComponent,
    SegmentationResultImgComponent
  ],
  imports: [
    CommonModule,
    TigerRoutingModule,
    FontAwesomeModule,
    FormsModule,
    ModalModule.forRoot(),
    ProgressbarModule.forRoot(),
    TooltipModule.forRoot()
  ],
  providers: [
    DetectionService,
    SegmentationService
  ]
})
export class TigerModule { }
