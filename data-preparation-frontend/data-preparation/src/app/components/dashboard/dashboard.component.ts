import {
  Component,
  EventEmitter,
  OnDestroy,
  OnInit,
  Output,
} from '@angular/core';
import { DashboardService } from '../../services/dashboard.service';
import { MatDialog } from '@angular/material/dialog';
import { ModuleConfigDialogComponent } from '../dialogs/module-config-dialog/module-config-dialog.component';
import { Subject, mergeMap, of, switchMap, takeUntil } from 'rxjs';
import { PreviewDialogComponent } from '../dialogs/preview-dialog/preview-dialog.component';
import { NetworkService } from '../../services/network.service';
import { ModuleInstance } from 'src/app/models/network';
import { ProjectService } from 'src/app/services/project.service';
import { ActionDialogComponent } from '../dialogs/action-dialog/action-dialog.component';
import { NotificationService } from 'src/app/services/notification.service';
import { HelpDialog } from '../dialogs/help-dialog/help-dialog.component';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
})
export class DashboardComponent implements OnInit, OnDestroy {
  private destroy$: Subject<void> = new Subject<void>();

  @Output() themeToggle: EventEmitter<any> = new EventEmitter();

  // indicator that request is in progress
  isLoading: boolean = false;
  // loading spinner is shown only once delay is expired
  // this ensures that there is no flickering if requests are completed fast.
  delayExpired: boolean = false;
  // delay in ms
  delayMs: number = 300;

  constructor(
    public readonly dashboardService: DashboardService,
    public readonly networkService: NetworkService,
    public readonly projectService: ProjectService,
    public readonly notificationService: NotificationService,
    public dialog: MatDialog
  ) {}

  ngOnInit(): void {
    // setup project
    this.projectService
      .getOrCreateProject()
      .pipe(takeUntil(this.destroy$))
      .subscribe();

    // setup modules
    this.projectService.project$
      .pipe(
        switchMap(() => this.networkService.setupModules()),
        takeUntil(this.destroy$)
      )
      .subscribe();

    // setup network
    this.networkService
      .setupNetwork()
      .pipe(takeUntil(this.destroy$))
      .subscribe();

    // module dialog
    this.dashboardService.openDialog$
      .pipe(
        mergeMap((moduleInstance: ModuleInstance) => {
          const dialogRef = this.dialog.open(ModuleConfigDialogComponent, {
            data: { moduleInstance },
          });

          return dialogRef.afterClosed();
        }),
        takeUntil(this.destroy$)
      )
      .subscribe();

    // open preview dialog
    this.dashboardService.openPreviewDialog$
      .pipe(
        mergeMap((moduleInstance: ModuleInstance) => {
          const dialogRef = this.dialog.open(PreviewDialogComponent, {
            // prohibit multiple open preview dialogs until we properly support it
            // with refresh and verification that same preview cannot be opened multiple times
            // hasBackdrop: false,
            // disableClose: true,
            data: { moduleInstance: moduleInstance },
          });

          return dialogRef.afterClosed();
        }),
        takeUntil(this.destroy$)
      )
      .subscribe();
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  getProjectName(): string {
    return this.dashboardService.currentProject
      ? this.dashboardService.currentProject
      : 'Unknown';
  }

  onTaskDescriptionClick() {
    this.dialog.open(HelpDialog, {
      data: {
        title: 'Help',
      },
      id: 'help-dialog',
      hasBackdrop: false,
      minWidth: '500px',
      maxWidth: '30vw',
      position: { top: '40px', right: '10px' },
    });
  }

  onMenuNewClick() {
    const dialogRef = this.dialog.open(ActionDialogComponent, {
      data: {
        title: 'Are you sure you want to proceed?',
        description:
          'The current network will be replaced by an empty network.',
      },
    });

    dialogRef
      .afterClosed()
      .pipe(
        mergeMap((confirm: boolean) => {
          if (confirm) {
            return this.networkService.resetToEmptyNetwork();
          } else {
            return of(false);
          }
        }),
        takeUntil(this.destroy$)
      )
      .subscribe();
  }

  onRunAllClick() {
    this.isLoading = true;
    this.delayExpired = false;

    setTimeout(() => {
      this.delayExpired = true;
    }, this.delayMs);

    this.networkService
      .runNetwork()
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: ({ response }) => {
          this.isLoading = false;
          this.delayExpired = false;

          if (response.ok) {
            this.notificationService.showInfo('Execution complete 🚀');
          } else {
            this.notificationService.showError(
              `Failed to execute network - ${response.status}`
            );
          }
        },
        error: (_) => {
          this.notificationService.showError('Failed to execute network');
          this.isLoading = false;
          this.delayExpired = false;
        },
      });
  }

  onThemeClick() {
    this.themeToggle.emit();
  }

  goToWorkflowPage() {
    window.location.href =
      environment.workflowPageBasePath + `?projectId=${this.getProjectName()}`;
  }
}
