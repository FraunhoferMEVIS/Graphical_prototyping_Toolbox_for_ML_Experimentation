import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { DashboardService } from '../../workflow-dashboard/workflow-dashboard.service';

interface DialogData {
  title: string;
}

@Component({
  selector: 'app-select-project-dialog',
  templateUrl: './manage-project-dialog.component.html',
  styleUrls: ['./manage-project-dialog.component.scss'],
})
export class ManageProjectDialogComponent {

  constructor(
    public dialogRef: MatDialogRef<ManageProjectDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData,
    public dashboardService: DashboardService
  ) {
  }

  onSubmit() {
    this.dialogRef.close();
  }
}
