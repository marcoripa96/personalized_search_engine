import { trigger, transition, style, animate, animateChild, query, stagger } from '@angular/animations';
import { Component, Input, OnInit, ViewEncapsulation } from '@angular/core';
import { Hit } from 'src/app/shared/interfaces/hit';

@Component({
  selector: 'app-hits-list',
  templateUrl: './hits-list.component.html',
  styleUrls: ['./hits-list.component.scss'],
  encapsulation: ViewEncapsulation.None,
  animations: [
    trigger('list', [
      transition(':enter', [
        query('@items', stagger(50, animateChild()))
      ]),
    ]),
    trigger('items', [
      transition(':enter', [
        style({ transform: 'scale(0.5)', opacity: 0 }),  // initial
        animate('300ms cubic-bezier(.8, -0.6, 0.2, 1.5)',
          style({ transform: 'scale(1)', opacity: 1 }))  // final
      ])
    ])
  ]
})
export class HitsListComponent implements OnInit {

  @Input() hits: Hit[];
  @Input() showMatches: boolean;

  constructor() { }

  ngOnInit(): void {
  }

}
