import { Component, EventEmitter, Input, OnInit, Output, ViewEncapsulation } from '@angular/core';
import { FormControl, FormGroup } from '@angular/forms';
import { Hit } from 'src/app/shared/interfaces/hit';
import { Preset } from 'src/app/shared/interfaces/preset';
import { UserHit } from 'src/app/shared/interfaces/user';
import { SearchService } from 'src/app/shared/services/search.service';

@Component({
  selector: 'app-search-bar',
  templateUrl: './search-bar.component.html',
  styleUrls: ['./search-bar.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class SearchBarComponent implements OnInit {

  @Input() users: UserHit[];
  @Input() currentUser: any;
  @Output() searchEvent: EventEmitter<Hit[]> = new EventEmitter();

  searchForm: FormGroup;

  searchUser = 'all';

  @Input() set currentPreset(preset: Preset) {
    if (preset) {
      this.searchForm.patchValue({
        mode: preset.mode,
        search: preset.query
      });
    }
  }

  get query(): string {
    return this.searchForm.get('search').value;
  }

  get mode(): FormControl {
    return this.searchForm.get('mode') as FormControl;
  }

  constructor(private searchService: SearchService) { }

  ngOnInit(): void {
    this.searchForm = this.createForm();
  }

  private createForm(): FormGroup {
    return  new FormGroup({
      search: new FormControl(''),
      mode: new FormControl('default')
    });
  }

  search(): void {
    const mode = this.mode.value;

    switch (mode) {
      case 'default': {
        this.searchService.search(this.query, this.searchUser).subscribe(res => {
          this.searchEvent.emit(res);
        });
        break;
      }
      case 'popularity': {
        this.searchService.searchByPopularity(this.query, this.searchUser).subscribe(res => {
          this.searchEvent.emit(res);
        });
        break;
      }
      case 'words': {
        this.searchService.searchWordsPreference(this.query, this.searchUser, this.currentUser.top_words,
          this.currentUser.top_entities).subscribe(res => {
          this.searchEvent.emit(res);
        });
        break;
      }
      case 'hashtags': {
        this.searchService.searchHashtagPreference(this.query, this.searchUser, this.currentUser.top_hashtags).subscribe(res => {
          this.searchEvent.emit(res);
        });
        break;
      }

    }
  }

  selectSearchUser(user?: string): void {
    this.searchUser = user;
  }

}
