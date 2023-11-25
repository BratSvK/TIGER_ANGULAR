import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DetectionComponent } from './components/detection/detection.component';


const routes: Routes = [
    {
        path: '',
        component: DetectionComponent
    }
];

@NgModule({
    imports: [RouterModule.forChild(routes)],
    exports: [RouterModule]
})
export class DetectionRoutingModule { }
