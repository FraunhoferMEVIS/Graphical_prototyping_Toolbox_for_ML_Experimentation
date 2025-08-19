import { Injectable, NgZone } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ErrorDialogComponent } from '../components/dialogs/error-dialog/error-dialog.component';

@Injectable({
  providedIn: 'root',
})
export class NotificationService {
  constructor(
    private snackbar: MatSnackBar,
    private dialog: MatDialog,
    private zone: NgZone
  ) {}

  showError(message: string): void {
    this.zone.run(() => {
      this.snackbar.open(`Error: ${message}`, 'Okay');
    });
  }

  showErrorAsDialog(message: string) {
    this.zone.run(() => {
      this.dialog.open(ErrorDialogComponent, {
        width: '30%',
        data: { title: 'Error 😥', description: message },
      });
    });
  }

  showInfo(message: string) {
    this.zone.run(() => {
      this.snackbar.open(message, 'Got it!');
    });
  }
}
