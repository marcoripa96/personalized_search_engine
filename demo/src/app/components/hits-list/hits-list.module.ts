import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HitsListComponent } from './hits-list.component';
import { MatIconModule } from '@angular/material/icon';

@NgModule({
  imports: [
    CommonModule,
    MatIconModule
  ],
  declarations: [HitsListComponent],
  exports: [HitsListComponent]
})
export class HitsListModule { }
