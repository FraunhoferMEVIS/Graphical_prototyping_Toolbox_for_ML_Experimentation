import { Injectable } from '@angular/core';
import { MethodSelectionService } from './method-selection.service';
import { ExecuteService } from '../backend-client';
import { ProgressSpinnerMode } from '@angular/material/progress-spinner';
import { Observable, first, timer, Subscription } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class RunStatusService {
  public loggedIn: boolean = false;
  public running: boolean = false;
  public jobsCreated: boolean = false;
  public progress: number = 0;

  constructor(
    private methodSelectionService: MethodSelectionService,
    private executeService: ExecuteService
  ) {}

  public runExperiment(): Observable<string> {
    this.running = true;
    return this.executeService.runAllExecuteAllPost(
      this.methodSelectionService.descriptionFormGroup.controls.name.value
    );
  }

  public updateStatus(): void {
    timer(0, 2000).subscribe(() => {
      let status: Subscription = this.executeService
        .getStatusExecuteStatusGet(
          this.methodSelectionService.descriptionFormGroup.controls.name.value
        )
        .pipe(first())
        .subscribe((res) => {
          let p: number = 0;
          let d: number = 0;
          for (const r of Object.keys(res)) {
            if (res[r].progress !== undefined && res[r].progress !== null) {
              p += res[r].progress;
              d += 1;
            }
          }
          this.progress = p / d;
          if (this.progress > 0) {
            this.jobsCreated = true;
          }
          if (this.progress >= 100) {
            this.running = false;
          }
          console.log(this.progress);
          status.unsubscribe();
        });
    });
  }

  public spinnerType(): ProgressSpinnerMode {
    if (this.jobsCreated) {
      return 'determinate';
    }
    return 'indeterminate';
  }
}
