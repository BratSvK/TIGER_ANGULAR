import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { NotFoundComponent } from './not-found/not-found.component';

const routes: Routes = [
    {
      path: '',
      loadChildren: () => import('./tiger/tiger.module').then(m => m.TigerModule),
    },
    {
      path: 'not-found',
      component: NotFoundComponent
    },
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
