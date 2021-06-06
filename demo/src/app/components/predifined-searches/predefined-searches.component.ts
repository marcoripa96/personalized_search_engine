import { Component, EventEmitter, Input, OnInit, Output, ViewEncapsulation } from '@angular/core';
import { Preset } from 'src/app/shared/interfaces/preset';

interface SearchConfig {
  query: string;
}

@Component({
  selector: 'app-predefined-searches',
  templateUrl: './predefined-searches.component.html',
  styleUrls: ['./predefined-searches.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class PredefinedSearchesComponent implements OnInit {

  @Input() preset: Preset;

  @Output() selected: EventEmitter<Preset> = new EventEmitter();

  constructor() { }

  ngOnInit(): void {
  }

  selectPreset(preset: Preset): void {
    this.selected.emit(preset);
  }

}
