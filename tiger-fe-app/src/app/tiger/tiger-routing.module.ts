import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { TigerComponent } from './component/tiger/tiger.component';
import { DetectionComponent } from '../detection/components/detection/detection.component';
import { SegmentationComponent } from '../segmentation/components/segmentation/segmentation.component';

const routes: Routes = [
  {
    path: 'home',
    component: TigerComponent,
    children: [
      {
        path: '',
        pathMatch: 'full',
        redirectTo: 'detection'
      },
      {
        path: 'detection',
        component: DetectionComponent
      },
      {
        path: 'segmentation',
        component: SegmentationComponent
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class TigerRoutingModule { }
