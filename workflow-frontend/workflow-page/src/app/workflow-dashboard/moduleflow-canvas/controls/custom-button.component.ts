import { Component, Input } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { ClassicPreset } from 'rete';

export class ButtonControl extends ClassicPreset.Control {
  constructor(public label: string, public onClick: () => void) {
    super();
  }
}

/**
 * Component must be standalone in order for
 * Angular material directives to work.
 */
@Component({
  selector: 'custom-control-button',
  styleUrls: ['./custom-button.component.css'],
  standalone: true,
  imports: [MatButtonModule],
  template: `<button
    mat-stroked-button
    color="primary"
    class="custom-control-button"
    (pointerdown)="$event.stopPropagation()"
    (dblclick)="$event.stopPropagation()"
    (click)="data.onClick()"
  >
    {{ data.label }}
  </button>`,
})
export class ButtonComponent {
  @Input() data: ButtonControl;
}
