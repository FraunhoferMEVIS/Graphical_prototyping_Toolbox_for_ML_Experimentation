import {
  Component,
  ElementRef,
  Injector,
  Input,
  OnChanges,
  OnDestroy,
  SimpleChanges,
  ViewChild,
  ViewEncapsulation,
} from '@angular/core';
import { Editor } from './editor';
import { Module } from '../models/module';
import { ModuleInstance } from '../models/module-instance';
import { Workflow } from '../models/workflow';
import { DashboardService } from '../workflow-dashboard.service';
import { Subscription } from 'rxjs';

interface Payload {
  x: number;
  y: number;
  module: Module;
}

@Component({
  selector: 'moduleflow-canvas',
  templateUrl: './moduleflow-canvas.component.html',
  styleUrls: ['./moduleflow-canvas.component.css'],
  encapsulation: ViewEncapsulation.None,
})
export class ModuleflowCanvasComponent implements OnChanges, OnDestroy {
  constructor(
    private injector: Injector,
    private dashboardService: DashboardService
  ) {}

  @ViewChild('rete') container!: ElementRef;
  @Input() workflow!: Workflow;
  @Input() project: string;

  private editor: Editor;

  private subscription: Subscription;

  ngOnChanges(changes: SimpleChanges): void {
    var importWorkflow = false;

    // only react to changes if we already initialized the editor
    // otherwise makes no sense to do anything
    if (this.editor) {
      if (changes['project'] && changes['project'].currentValue) {
        this.editor.project = changes['project'].currentValue;
        importWorkflow = true;
      }

      if (changes['workflow']) {
        importWorkflow = true;
      }

      if (importWorkflow) {
        this.editor.importWorkflow(this.workflow);
      }
    }
  }

  ngAfterViewInit(): void {
    const el = this.container.nativeElement;
    if (el) {
      this.editor = new Editor(el, this.injector, this.project ?? '');
      if (this.workflow) {
        this.editor.importWorkflow(this.workflow);
      }
    }

    this.subscription = this.dashboardService.updatedModules$.subscribe(() => {
      this.editor?.updateNodes();
    });
  }

  ngOnDestroy(): void {
    this.subscription?.unsubscribe();
  }

  addModule(payload: Payload) {
    const instance = ModuleInstance.fromModule(payload.module);
    this.editor.addModule(payload.x, payload.y, instance);
  }
}
