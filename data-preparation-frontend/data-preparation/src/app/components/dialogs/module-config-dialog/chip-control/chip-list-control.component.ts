import { LiveAnnouncer } from '@angular/cdk/a11y';
import { Component, Input, inject } from '@angular/core';
import { FormControl } from '@angular/forms';
import { MatChipInputEvent } from '@angular/material/chips';
import { COMMA, ENTER } from '@angular/cdk/keycodes';
import { InputType } from '../module-config-dialog.component';

/**
 * Component that lets users enter a list of chips as input.
 *
 * The component encapsulates a material form field and can be integrated into any formGroup.
 */
@Component({
  selector: 'app-chip-list-control',
  templateUrl: './chip-list-control.component.html',
  styleUrls: ['./chip-list-control.component.css'],
})
export class ChipListControlComponent {
  @Input() control: FormControl;
  @Input() error?: string;
  @Input() label: string;
  @Input() required: boolean = false;
  @Input() type: InputType;
  @Input() description: string;

  readonly separatorKeysCodes = [ENTER, COMMA] as const;

  _values: string[];

  @Input()
  set values(values: string[]) {
    this._values = values == null ? [] : [...values];
  }

  get values(): string[] {
    return this._values;
  }

  announcer = inject(LiveAnnouncer);

  remove(value: string) {
    const index = this.values.indexOf(value);
    if (index >= 0) {
      this.values.splice(index, 1);
      this.announcer.announce(`removed ${value}`);
    }
  }

  add(event: MatChipInputEvent): void {
    const value = (event.value || '').trim();
    if (value) {
      this.values.push(value);
    }

    event.chipInput!.clear();
  }
}
