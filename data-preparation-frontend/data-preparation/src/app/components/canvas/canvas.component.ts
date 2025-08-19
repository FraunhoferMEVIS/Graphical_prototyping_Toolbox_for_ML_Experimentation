import {
  AfterViewInit,
  Component,
  ElementRef,
  Injector,
  Input,
  OnDestroy,
  SimpleChanges,
  ViewChild,
  ViewEncapsulation,
} from '@angular/core';
import { Editor, EditorEvent, EventType } from './editor';
import { NetworkViewModel } from '../../models/network';
import { NetworkService } from '../../services/network.service';
import { Subject, switchMap, takeUntil } from 'rxjs';
import { ModuleBlueprint } from 'src/app/api/data-preparation/api.service';
import { NotificationService } from 'src/app/services/notification.service';

interface DroppablePayload {
  x: number;
  y: number;
  dragData: ModuleBlueprint;
}

@Component({
  selector: 'app-canvas',
  templateUrl: './canvas.component.html',
  styleUrls: ['./canvas.component.css'],
  encapsulation: ViewEncapsulation.None,
})
export class CanvasComponent implements AfterViewInit, OnDestroy {
  private destroy$: Subject<void> = new Subject<void>();
  private editor: Editor;

  @ViewChild('rete') container!: ElementRef;
  @Input() network: NetworkViewModel;
  @Input() modules: Array<ModuleBlueprint>;

  constructor(
    private injector: Injector,
    private networkService: NetworkService,
    private notificationService: NotificationService
  ) {}

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['network'] && this.editor) {
      const currentNetwork = changes['network'].currentValue;
      currentNetwork ? this.editor.import(currentNetwork) : this.editor.clear();
    }

    if (changes['modules'] && this.editor) {
      const newModules = changes['modules']
        .currentValue as Array<ModuleBlueprint>;
      if (newModules.length >= 0) {
        this.editor.populateMenu(newModules);
      }
    }
  }

  ngAfterViewInit(): void {
    const el = this.container.nativeElement;
    if (el) {
      this.editor = new Editor(el, this.injector);

      if (this.network) {
        this.editor.import(this.network);
      }
    }

    // Update a specific node
    this.networkService.updatedModule$
      .pipe(takeUntil(this.destroy$))
      .subscribe((m) => {
        this.editor.updateNode(m.id, m);
      });

    // React to events emitted by the editor.
    // E.g. errors, notifications, callToAction, etc...
    this.editor.events$
      .pipe(takeUntil(this.destroy$))
      .subscribe((event: EditorEvent) => {
        if (event.type == EventType.ERROR) {
          this.notificationService.showError(event.message);
        }
      });

    // React to save network event.
    this.networkService.onSaveNetwork$
      .pipe(
        switchMap(() => {
          var network = this.editor.export();
          return this.networkService.saveNetwork(network);
        }),
        takeUntil(this.destroy$)
      )
      .subscribe(() => {});
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  async onItemDropped(payload: DroppablePayload) {
    await this.editor.addModule(payload.dragData);
  }
}
