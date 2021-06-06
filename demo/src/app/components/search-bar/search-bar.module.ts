import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SearchBarComponent } from './search-bar.component';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { ReactiveFormsModule } from '@angular/forms';
import { MatRadioModule } from '@angular/material/radio';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatMenuModule } from '@angular/material/menu';

@NgModule({
  imports: [
    CommonModule,
    MatIconModule,
    MatButtonModule,
    ReactiveFormsModule,
    MatRadioModule,
    MatSelectModule,
    MatFormFieldModule,
    MatMenuModule
  ],
  declarations: [SearchBarComponent],
  exports: [SearchBarComponent]
})
export class SearchBarModule { }
