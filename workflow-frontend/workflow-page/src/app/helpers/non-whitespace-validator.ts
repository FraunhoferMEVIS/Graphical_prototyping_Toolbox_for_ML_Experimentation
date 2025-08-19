import { FormControl } from '@angular/forms';

export function noWhitespaceValidator(control: FormControl) {
  return (control.value || '').trim().length ? null : { whitespace: true };
}
