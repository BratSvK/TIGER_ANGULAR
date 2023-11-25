import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { NotFoundComponent } from './not-found/not-found.component';

const routes: Routes = [
    {
      path: 'detection',
      loadChildren: () => import('./detection/detection.module').then(m => m.DetectionModule),
    },
    {
      path: 'segmentation',
      loadChildren: () => import('./segmentation/semgmentation.module').then(m => m.SegmentationModule),
    },
    {
      path: 'not-found',
      component: NotFoundComponent
    },
    // {
    //   path: 'server-error',
    //   component: ServerErrorComponent
    // },
    {
      path: '**', component: NotFoundComponent,
      pathMatch: 'full'
    }
  ];
  
  @NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
  })
  export class AppRoutingModule { }
