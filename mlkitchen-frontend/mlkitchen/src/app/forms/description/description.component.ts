import { Component, Input } from '@angular/core';
import { MethodSelectionService } from '../../services/method-selection.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { OnInit, OnDestroy } from '@angular/core';

@Component({
  selector: 'app-description',
  templateUrl: './description.component.html',
  styleUrls: ['./description.component.scss'],
})
export class DescriptionComponent implements OnInit, OnDestroy {
  @Input() public formGroup: any;

  constructor(
    private _snackBar: MatSnackBar,
    public methodSelectionService: MethodSelectionService
  ) {}

  ngOnInit(): void {}

  openSnackBar(message: string, action: string) {
    this._snackBar.open(message, action);
  }

  changeExperimentType(name, features) {
    if (features !== undefined) {
      const feature = features.find((f) => f.name === name);
      if (feature.type === 'numerical') {
        this.formGroup.controls.type.setValue('regression');
      } else {
        this.formGroup.controls.type.setValue('classification');
      }
      this.openSnackBar('Estimator setting may no longer be valid.', 'close');
    }
  }

  getExperimentType(description) {
    if (description && description.features) {
      const feature = description.features.find(
        (f) => f.name === this.formGroup.controls.target.value
      );
      if (feature && feature.type === 'numerical') {
        this.formGroup.controls.type.setValue('regression');
      } else if (feature && feature.type === 'categorical') {
        this.formGroup.controls.type.setValue('classification');
      }
      return this.formGroup.controls.type.value;
    }
    return null;
  }

  ngOnDestroy(): void {}
}
