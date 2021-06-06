import { Component, HostListener, OnInit, ViewEncapsulation } from '@angular/core';
import { MatSlideToggleChange } from '@angular/material/slide-toggle';
import { Hit } from './shared/interfaces/hit';
import { Preset } from './shared/interfaces/preset';
import { User, UserHit } from './shared/interfaces/user';
import { SearchService } from './shared/services/search.service';
import { PRESETS } from './shared/static/presets';
import { USERS_DETAILS } from './shared/static/users';



@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class AppComponent implements OnInit {

  elasticStatus: boolean;

  userHits: UserHit[];
  usersDetails = USERS_DETAILS;
  currentUser: any;
  currentColor: string;

  presets = PRESETS;
  currentPreset: Preset;

  scrolled = false;

  showMatchesVar: boolean;

  hits: Hit[];

  constructor(private searchService: SearchService){}

  ngOnInit(): void {
    this.currentUser = this.anonymUser();
    this.searchService.getAllUsers().subscribe(res => {
      this.userHits = res;
    });
  }

  searchResults(hits: Hit[]): void {
    this.hits = hits;
  }

  selectUser(index: number, user: User): void {
    this.currentUser = user;
    this.currentColor = this.usersDetails[index].color;
    this.hits = [];
  }

  signout(): void {
    this.currentUser = this.anonymUser();
    this.hits = [];
  }

  selectPreset(preset: Preset): void {
    this.currentUser = preset.currentUser === 6 ? this.anonymUser() : this.userHits[preset.currentUser]._source;
    this.currentPreset = preset;
  }

  showMatches(event: MatSlideToggleChange): void {
    this.showMatchesVar = event.checked;
  }


  private anonymUser(): any {
    return {
      username: 'anonymous',
      initials: 'AN',
      color: 'gray'
    };
  }

  @HostListener('window:scroll', ['$event']) // for window scroll events
  scroll(event): void {
    if (this.currentUser.username === 'anonymous') {
      if (window.pageYOffset > 70) {
        this.scrolled = true;
      } else {
        this.scrolled = false;
      }
    } else {
      if (window.pageYOffset > 255) {
        this.scrolled = true;
      } else {
        this.scrolled = false;
      }
    }

  }


}
