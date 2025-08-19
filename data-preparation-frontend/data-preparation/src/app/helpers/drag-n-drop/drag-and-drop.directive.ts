import { Directive, ElementRef, EventEmitter, HostListener, Input, OnInit, Output } from '@angular/core';
import interact from 'interactjs';

@Directive({
  selector: '[draggable]'
})
/**
 * https://www.auroria.io/interactjs-in-angular/
 */
export class Draggable implements OnInit {

  @Input()
  dragData: any;

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
      .draggable(Object.assign({}, this.options || {}))
      .on('dragmove', (event) => {
        const target = event.target;
        const x = (parseFloat(target.getAttribute('data-x')) || 0) + event.dx;
        const y = (parseFloat(target.getAttribute('data-y')) || 0) + event.dy;

        target.style.transform = 'translate(' + x + 'px, ' + y + 'px)';
        target.setAttribute('data-x', x);
        target.setAttribute('data-y', y);

        target.classList.add('getting-dragged');
        this.currentlyDragged = true;
        (window as any).dragData = this.dragData;
      })
      .on('dragend', (event) => {
        event.target.style.transform = 'none';
        event.target.removeAttribute('data-x');
        event.target.removeAttribute('data-y');
        event.target.classList.remove('getting-dragged');
        setTimeout(() => {
          (window as any).dragData = null;
          this.currentlyDragged = false;
        });
      });
  }
}


@Directive({
  selector: '[droppable]'
})
/**
 * https://www.auroria.io/interactjs-in-angular/
 */
export class Droppable implements OnInit {

  @Input()
  options: any;

  @Output()
  dropping: EventEmitter<any> = new EventEmitter();

  constructor(private elementRef: ElementRef) { }

  ngOnInit(): void {
    interact(this.elementRef.nativeElement)
      .dropzone(Object.assign({}, this.options || {}))
      .on('dropactivate', event => event.target.classList.add('can-drop'))
      .on('dragenter', event => {

        const draggableElement = event.relatedTarget;
        const dropzoneElement = event.target;

        dropzoneElement.classList.add('can-catch');
        draggableElement.classList.add('drop-me');

      })
      .on('dragleave', event => {
        event.target.classList.remove('can-catch', 'caught-it');
        event.relatedTarget.classList.remove('drop-me');
      })
      .on('drop', event => {
        // calculate x,y position inside dropzone
        // https://stackoverflow.com/a/45108136
        var dropzonePostion = event.target.getBoundingClientRect();
        var elementPosition = event.relatedTarget.getBoundingClientRect();
        var x = elementPosition.left - dropzonePostion.left;
        var y = elementPosition.top - dropzonePostion.top;

        const dragData = (window as any).dragData;
        if (typeof (dragData) === 'object') {
          this.dropping.emit({ x: x, y: y, dragData: dragData });
        } else {
          console.warn("dropped without data")
        }

        event.target.classList.add('caught-it');

        if ((window as any).document.selection) {
          (window as any).document.selection.empty();
        } else {
          window.getSelection()!.removeAllRanges();
        }
      })
      .on('dropdeactivate', event => {
        event.target.classList.remove('can-drop');
        event.target.classList.remove('can-catch');
      });
  }
}