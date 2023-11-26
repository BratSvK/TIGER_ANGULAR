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


@NgModule({
  declarations: [
    TigerComponent,
    DetectionComponent,
    SegmentationComponent,
    NavbarComponent,
    ImageUploaderComponent
  ],
  imports: [
    CommonModule,
    TigerRoutingModule,
    FontAwesomeModule,
    ModalModule.forRoot()
  ]
})
export class TigerModule { }
