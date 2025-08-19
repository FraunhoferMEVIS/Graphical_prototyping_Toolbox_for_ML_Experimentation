import { Directive, ElementRef, EventEmitter, HostListener, Input, OnInit, Output } from '@angular/core';
import interact from 'interactjs';

@Directive({
  selector: '[moveable]'
})
/**
 * https://www.auroria.io/interactjs-in-angular/
 */
export class Moveable implements OnInit {

  @Input()
  model: any;

  @Input()
  options: any;

  @Output()
  draggableClick = new EventEmitter();

  private currentlyDragged = false;

  constructor(private element: ElementRef) { }

  @HostListener('click', ['$event'])
  public onClick(event: any): void {
    if (!this.currentlyDragged) {
      this.draggableClick.emit();
    }
  }

  ngOnInit(): void {
    interact(this.element.nativeElement)
      .draggable(Object.assign({}, this.options || {
        // enable inertial throwing
        inertia: true,
        // keep the element within the area of it's parent
        modifiers: [
          interact.modifiers.restrictRect({
            restriction: 'parent',
            endOnly: true
          })
        ],
      }))
      .on('dragmove', (event) => {
        const target = event.target;
        const x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx;
        const y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy;

        target.style.transform = 'translate(' + x + 'px, ' + y + 'px)';
        target.setAttribute('data-x', x);
        target.setAttribute('data-y', y);

        target.classList.add('getting-moved');
        this.currentlyDragged = true;
      })
      .on('dragend', (event) => {
        event.target.removeAttribute('data-x');
        event.target.removeAttribute('data-y');
        event.target.classList.remove('getting-moved');
        setTimeout(() => {
          this.currentlyDragged = false;
        });
      });
  }
}
