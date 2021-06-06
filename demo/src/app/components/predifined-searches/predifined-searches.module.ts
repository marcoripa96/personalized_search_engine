import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { PredefinedSearchesComponent } from './predefined-searches.component';
import {MatCardModule} from '@angular/material/card';

@NgModule({
  imports: [
    CommonModule,
    MatCardModule
  ],
  declarations: [PredefinedSearchesComponent],
  exports: [PredefinedSearchesComponent]
})
export class PredefinedSearchesModule { }
