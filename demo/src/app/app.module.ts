import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { Client } from 'elasticsearch-browser/elasticsearch';
import { SearchBarModule } from './components/search-bar/search-bar.module';
import { HitsListModule } from './components/hits-list/hits-list.module';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatMenuModule } from '@angular/material/menu';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { PredefinedSearchesModule } from './components/predifined-searches/predifined-searches.module';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';
import { environment } from './../environments/environment';


@NgModule({
  declarations: [
    AppComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    SearchBarModule,
    MatToolbarModule,
    PredefinedSearchesModule,
    MatMenuModule,
    HitsListModule,
    MatIconModule,
    MatChipsModule,
    MatSlideToggleModule
  ],
  providers: [
    {
      provide: 'elasticsearch',
      useFactory: () => {
        return new Client({
          host: environment.elasticUrl
        });
      },
      deps: [],
    }
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
