import { ErrorHandler, Injectable, Injector } from '@angular/core';
import { HttpErrorResponse } from '@angular/common/http';

import { NotificationService } from '../services/notification.service';

@Injectable()
export class GlobalErrorHandler implements ErrorHandler {
  constructor(private injector: Injector) {}

  handleError(error: Error | HttpErrorResponse) {
    const notificationService = this.injector.get(NotificationService);

    let message: string;

    // Angular HttpClient error
    if (error instanceof HttpErrorResponse) {
      notificationService.showErrorAsDialog(error.message);
    } else {
      // any other error
      message = error.message ? error.message : error.toString();
      notificationService.showErrorAsDialog(message);
    }

    console.error(message);
  }
}
