import {
  trigger,
  state,
  stagger,
  style,
  transition,
  animate,
  keyframes,
  query,
} from '@angular/animations';

export const blendInOut = trigger('blendInOut', [
  transition(':enter', [
    style({ transform: 'translateX(100%)', opacity: 0 }),
    animate('250ms', style({ transform: 'translateX(0)', opacity: 1 })),
  ]),
  transition(':leave', [
    style({ transform: 'translateX(0)', opacity: 1 }),
    animate('250ms', style({ transform: 'translateX(100%)', opacity: 0 })),
  ]),
]);
