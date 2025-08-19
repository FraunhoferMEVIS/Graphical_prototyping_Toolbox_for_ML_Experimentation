import { Component } from '@angular/core';
import { MethodSelectionService } from '../services/method-selection.service';
import { blendInOut } from '../animations';
import { ActivatedRoute } from '@angular/router';
import { first } from 'rxjs';
import { MatSnackBar } from '@angular/material/snack-bar';
import { ExecuteService } from '../backend-client';
import { RunStatusService } from '../services/run-status.service';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'app-sidenav',
  templateUrl: './sidenav.component.html',
  styleUrls: ['./sidenav.component.scss'],
  animations: [blendInOut],
})
export class SidenavComponent {
  badgeHidde = false;
  username: string = '';
  password: string = '';

  constructor(
    private _snackBar: MatSnackBar,
    public methodSelectionService: MethodSelectionService,
    public route: ActivatedRoute,
    public executeService: ExecuteService,
    public runStatusService: RunStatusService
  ) {
    this.route.queryParamMap.subscribe((params) => {
      const project = params.get('projectId');
      if (project) {
        this.methodSelectionService.descriptionFormGroup.controls.name.setValue(
          project
        );
        this.methodSelectionService.loadExistingProject(project);
      }
    });
  }

  openSnackBar(message: string, action: string) {
    this._snackBar.open(message, action);
  }

  public saveExperiment() {
    this.methodSelectionService
      .postConfigToBackend()
      .pipe(first())
      .subscribe({
        next: (response) => {
          this.openSnackBar('Saved Experiment', 'close');
        },
        error: (error: HttpErrorResponse) => {
          this.openSnackBar(
            'Error when saving. Make sure all mandatory desciption fields and steps (Split, Estimator, Metrics) are defined.',
            'close'
          );
        },
      });
  }

  public runExperiment() {
    this.runStatusService
      .runExperiment()
      .pipe(first())
      .subscribe((res) => {
        this.runStatusService.updateStatus();
        this.openSnackBar(res, 'close');
      });
  }
}
