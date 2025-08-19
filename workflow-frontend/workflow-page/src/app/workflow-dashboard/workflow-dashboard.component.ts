import { Component } from '@angular/core';
import { DashboardService } from './workflow-dashboard.service';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'workflow-dashboard',
  templateUrl: './workflow-dashboard.component.html',
  styleUrls: ['./workflow-dashboard.css'],
})
export class WorkflowDashboardComponent {
  projectSelected: boolean = false;
  loading: boolean = false;

  constructor(
    public readonly dashboardService: DashboardService,
    private _snackBar: MatSnackBar
  ) {
    // initial loading of projects & set up of selected project
    this.loading = true;
    this.dashboardService
      .loadProjects()
      .pipe(takeUntilDestroyed())
      .subscribe((p) => {
        this.loading = false;

        const project = dashboardService.getProjectFromPath();
        if (project == null) {
          return;
        }

        const fetchedProject = p.find((p) => p == project);
        if (fetchedProject == null) {
          this._snackBar.open('Unknown project: ' + project, 'Ok');
          // reset project selection
          this.dashboardService.selectProject(null);
        } else {
          this.dashboardService.selectProject(fetchedProject);
        }
      });

    // update view once project selection changed
    this.dashboardService.selectedProject$
      .pipe(takeUntilDestroyed())
      .subscribe((p) => {
        this.projectSelected = p != null;
      });
  }
}
