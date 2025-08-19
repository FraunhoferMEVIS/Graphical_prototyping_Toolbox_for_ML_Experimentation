import { KeyValue } from '@angular/common';
import {
  ChangeDetectorRef,
  Component,
  HostBinding,
  Input,
  OnChanges,
  OnDestroy,
} from '@angular/core';
import { ModuleNode } from '../nodes';
import { DashboardService } from 'src/app/services/dashboard.service';
import { NetworkService } from 'src/app/services/network.service';
import { ModuleCategory } from 'src/app/api/data-preparation/api.service';
import { Subject, takeUntil } from 'rxjs';
import { NotificationService } from 'src/app/services/notification.service';

@Component({
  selector: 'app-custom-node',
  templateUrl: './custom-node.component.html',
  styleUrls: ['./custom-node.component.scss'],
  host: {
    class: 'module-node',
    'data-testid': 'node',
  },
})
export class CustomNodeComponent implements OnChanges, OnDestroy {
  @Input() data!: ModuleNode;
  @Input() emit!: (data: any) => void;
  @Input() rendered!: () => void;

  isRunning: boolean = false;

  private destroy$: Subject<void> = new Subject<void>();

  seed = 0;

  @HostBinding('class.selected') get selected() {
    return this.data.selected;
  }

  @HostBinding('class') get className() {
    return `${this.getColor(this.data.moduleInstance.blueprint.category)}`;
  }

  constructor(
    private cdr: ChangeDetectorRef,
    private readonly dashboardService: DashboardService,
    private readonly networkService: NetworkService,
    private readonly notificationService: NotificationService
  ) {
    // TODO: this was used in rete.js examples but it disables Angular's change detection
    //  this is usually enabled to prevent performance issues
    // as long as we don't notice any this can stay disabled.
    // this.cdr.detach();
  }

  ngOnChanges(): void {
    this.cdr.detectChanges();
    requestAnimationFrame(() => this.rendered());
    this.seed++; // force render sockets
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  sortByIndex<
    N extends object,
    T extends KeyValue<string, N & { index?: number }>,
  >(a: T, b: T) {
    const ai = a.value.index || 0;
    const bi = b.value.index || 0;

    return ai - bi;
  }

  getColor(category: ModuleCategory): string {
    switch (category) {
      case 'Filter': {
        return 'type-filter';
      }
      case 'Table': {
        return 'type-table';
      }
      case 'Table-Merge': {
        return 'type-table-merge';
      }
      case 'Preprocess': {
        return 'type-preprocess';
      }
      case 'Visualize': {
        return 'type-visualize';
      }
      case 'Aggregate and Transform': {
        return 'type-aggregate-and-transform';
      }
      default: {
        return '';
      }
    }
  }

  getIcon(category: ModuleCategory): string {
    switch (category) {
      case 'Filter': {
        return 'filter_alt';
      }
      case 'Table': {
        return 'table_view';
      }
      case 'Table-Merge': {
        return 'call_merge';
      }
      case 'Preprocess': {
        return 'science';
      }
      case 'Visualize': {
        return 'scatter_plot';
      }
      case 'Aggregate and Transform': {
        return 'transform';
      }
      default: {
        return '';
      }
    }
  }

  openConfig() {
    this.dashboardService.openDialog(this.data.moduleInstance);
  }

  openPreview() {
    this.dashboardService.openPreview(this.data.moduleInstance);
  }

  runModule() {
    this.isRunning = true;

    this.networkService
      .runModule(this.data.moduleInstance.module.id)
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: ({ error, response }) => {
          this.isRunning = false;

          if (error) {
            // TODO: change API model so that error obj is defined!
            const errorObj = error as unknown as { detail: string };
            this.notificationService.showErrorAsDialog(
              'detail' in errorObj
                ? errorObj.detail
                : 'Failed to execute module - status: ' + response.status
            );
          }
        },
        error: (error) => {
          this.isRunning = false;
          throw error;
        },
      });
  }

  stopModule() {
    this.notificationService.showInfo('Stop action is not supported yet.');
    // TODO: use stop action once implemented or remove it if stop won't be supported
    this.networkService
      .stopModule(this.data.moduleInstance.module.id)
      .pipe(takeUntil(this.destroy$))
      .subscribe();
  }
}
