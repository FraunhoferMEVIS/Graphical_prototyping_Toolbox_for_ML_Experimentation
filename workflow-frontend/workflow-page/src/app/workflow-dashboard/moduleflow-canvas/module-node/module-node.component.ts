import {
  Component,
  Input,
  HostBinding,
  ChangeDetectorRef,
  OnChanges,
  OnDestroy,
} from '@angular/core';
import { KeyValue } from '@angular/common';
import { ModuleNode } from '../module-node';
import { DashboardService } from '../../workflow-dashboard.service';
import { ModuleType } from '../../models/module-type';
import { Subscription } from 'rxjs';
import { ExecutionState } from '../../models/execution-state';

@Component({
  templateUrl: './module-node.component.html',
  styleUrls: ['./module-node.component.scss'],
  host: {
    class: 'module-node',
    'data-testid': 'node',
  },
})
export class ModuleNodeComponent implements OnChanges, OnDestroy {
  @Input() data!: ModuleNode;
  @Input() emit!: (data: any) => void;
  @Input() rendered!: () => void;

  subscription: Subscription;

  ModuleType = ModuleType;
  ExecutionState = ExecutionState;

  seed = 0;

  @HostBinding('class.selected') get selected() {
    return this.data.selected;
  }

  constructor(
    private cdr: ChangeDetectorRef,
    private dashboardService: DashboardService
  ) {
    this.cdr.detach();
  }

  ngOnChanges(): void {
    this.cdr.detectChanges();
    requestAnimationFrame(() => this.rendered());
    this.seed++; // force render sockets
  }

  ngOnDestroy(): void {
    this.subscription?.unsubscribe();
  }

  sortByIndex<
    N extends object,
    T extends KeyValue<string, N & { index?: number }>
  >(a: T, b: T) {
    const ai = a.value.index || 0;
    const bi = b.value.index || 0;

    return ai - bi;
  }
}
