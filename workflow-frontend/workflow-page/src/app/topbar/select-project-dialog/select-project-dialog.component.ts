import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { DashboardService } from '../../workflow-dashboard/workflow-dashboard.service';
import { take } from 'rxjs';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';

interface DialogData {
  title: string;
}

@Component({
  selector: 'app-select-project-dialog',
  templateUrl: './select-project-dialog.component.html',
  styleUrls: ['./select-project-dialog.component.scss'],
})
export class SelectProjectDialogComponent {
  selectedProject = null;

  constructor(
    public dialogRef: MatDialogRef<SelectProjectDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData,
    public dashboardService: DashboardService
  ) {
    dashboardService.selectedProject$
      .pipe(take(1), takeUntilDestroyed())
      .subscribe((p) => {
        this.selectedProject = p;
      });
  }

  onProjectSelected(event) {}

  onSubmit() {
    this.dashboardService.selectProject(this.selectedProject);
    this.dialogRef.close();
  }
}
