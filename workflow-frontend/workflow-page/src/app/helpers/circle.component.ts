

import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'svg-circle',
  template: `
    <svg [attr.width]="w" [attr.height]="h">
      <circle [attr.cx]="w/2" [attr.cy]="h/2" [attr.r]="r" stroke="black" [attr.stroke-width]="strokewidth" fill="none" />
    </svg>
  `
})
export class SvgCircleComponent implements OnInit {

  @Input() r: number = 0;

  w: number = 0;
  h: number = 0;
  strokewidth: number = 2.5;

  ngOnInit(): void {
    this.w = 2 * this.r + 2 * this.strokewidth;
    this.h = 2 * this.r + 2 * this.strokewidth;
  }



}