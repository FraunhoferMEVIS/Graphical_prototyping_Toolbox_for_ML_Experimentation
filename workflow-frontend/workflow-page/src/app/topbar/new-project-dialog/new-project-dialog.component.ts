import { Component, DestroyRef, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { DashboardService } from '../../workflow-dashboard/workflow-dashboard.service';
import { catchError, of } from 'rxjs';
import { FormControl, Validators } from '@angular/forms';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { HttpErrorResponse } from '@angular/common/http';
import { noWhitespaceValidator } from 'src/app/helpers/non-whitespace-validator';

interface DialogData {
  title: string;
}

@Component({
  selector: 'app-new-project-dialog',
  templateUrl: './new-project-dialog.component.html',
  styleUrls: ['./new-project-dialog.component.scss'],
})
export class NewProjectDialogComponent {
  projectName: FormControl = new FormControl('', [
    Validators.required,
    noWhitespaceValidator,
  ]);
  error: string = '';
  pattern = '^[a-zA-Z0-9-\\s]+$';

  constructor(
    public dialogRef: MatDialogRef<NewProjectDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData,
    private dashboardService: DashboardService,
    public destroyRef: DestroyRef
  ) {}

  getErrorMessage() {
    if (!this.projectName.dirty) {
      return '';
    }

    if (this.projectName.hasError('required')) {
      return 'Name must not be empty';
    }

    if (
      this.projectName.hasError('pattern') ||
      this.projectName.hasError('whitespace')
    ) {
      return 'Invalid character combination used.';
    }

    return '';
  }

  onSubmit() {
    const projectName = this.projectName.value;
    this.error = null;

    this.dashboardService
      .createProject(projectName)
      .pipe(
        takeUntilDestroyed(this.destroyRef),
        catchError((err, _) => {
          if (err instanceof HttpErrorResponse) {
            this.error = err.error.detail ?? `${err.status} - Unkown error`;
          } else {
            this.error = 'Unknown error';
          }

          return of(false);
        })
      )
      .subscribe((success) => {
        if (success) {
          this.dialogRef.close(success);
        } else {
          if (this.error === null) {
            this.error = 'Failed to save project. Try again later.';
          }
        }
      });
  }
}
