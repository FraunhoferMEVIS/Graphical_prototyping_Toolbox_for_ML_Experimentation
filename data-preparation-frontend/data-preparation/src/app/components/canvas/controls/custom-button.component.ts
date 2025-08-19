import { Component, Input } from "@angular/core";
import { ClassicPreset } from "rete";

export class ButtonControl extends ClassicPreset.Control {
  constructor(public label: string, public onClick: () => void) {
    super();
  }
}

@Component({
  selector: "custom-control-button",
  styleUrls: ["./custom-button.component.css"],
  template: `<button class="custom-control-button btn"
    (pointerdown)="$event.stopPropagation()"
    (dblclick)="$event.stopPropagation()"
    (click)="data.onClick()"
  >
    {{ data.label }}
  </button>`
})
export class ButtonComponent {
  @Input() data: ButtonControl;
}