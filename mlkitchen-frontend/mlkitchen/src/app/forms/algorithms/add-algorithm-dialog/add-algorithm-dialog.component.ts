import { Component, Inject, Input } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { Subscription, first } from 'rxjs';
import { Method, Parameter } from 'src/app/models/method';
import { Steps } from 'src/app/backend-client';
import { MethodSelectionService } from 'src/app/services/method-selection.service';

@Component({
  selector: 'app-add-algorithm-dialog',
  templateUrl: './add-algorithm-dialog.component.html',
  styleUrls: ['./add-algorithm-dialog.component.scss'],
})
export class AddAlgorithmDialogComponent {
  public supportedSteps: Steps[] = ['Estimator'];
  public tuningMethods: string[] = [];

  constructor(
    public dialogRef: MatDialogRef<AddAlgorithmDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: Method,
    public methodSelectionService: MethodSelectionService
  ) {
    this.methodSelectionService.hyperparameterTuning$
      .pipe(first())
      .subscribe((t) => {
        this.tuningMethods = t.algorithms[0].algorithms;
      });

    if (this.stepHasTuning(this.data.step)) {
      this.data.hyperParameterTuning = {
        iterations: 10,
        selectedTuningMethod: 'RandomizedSearchCV',
        parameters: [],
      };
    }

    for (let parameter of this.data.parameters) {
      if (parameter.default === 'NOT_FOR_FRONTEND') {
        this.data.parameters = this.data.parameters.filter(
          (p) => p.name != parameter.name
        );
      }

      if (parameter.default === 'MANDATORY_INPUT') {
        parameter.value = '';
        parameter.default = '';
        parameter.mandatory = true;
      }
    }

    for (let parameter of this.data.parameters) {
      if (parameter.default !== null && parameter.default !== undefined) {
        parameter.value = parameter.default;
      } else {
        parameter.value = 'None';
      }
      if (parameter.value === 'true') {
        parameter.value = true;
      }
      if (parameter.value === 'false') {
        parameter.value = false;
      }
    }

    if (this.data.step == 'HandlingMissingValues') {
      this.data.all_numerical = true;
    }

    if (this.data.step == 'Encoders') {
      if (this.methodSelectionService.encodersNumerical.includes(data.name)) {
        this.data.all_numerical = true;
      }
      if (this.methodSelectionService.encodersCategorical.includes(data.name)) {
        this.data.all_categorical = true;
      }
    }
  }

  onConfirm(): void {
    for (let parameter of this.data.parameters) {
      if (parameter.type === 'list[str]') {
        parameter.value = (parameter.value as string)
          .replace(/\s/g, '')
          .split(',');
      }
    }
    if (this.data.hyperParameterTuning?.parameters.length) {
      this.data = this.createTuning(this.data);
    }
    this.data = this.removeDefaultParameters(this.data);
    this.dialogRef.close({ event: 'submit', data: this.data });
  }

  onNoClick(): void {
    this.dialogRef.close({ event: 'cancel', data: this.data });
  }

  private removeDefaultParameters(data: Method): Method {
    for (let parameter of this.data.parameters) {
      if (
        parameter.value == undefined ||
        parameter.value == null ||
        parameter.value == 'None' ||
        parameter.default == parameter.value
      ) {
        data.parameters = data.parameters.filter(
          (p) => p.name != parameter.name
        );
      }
    }
    return data;
  }

  private createTuning(data: Method): Method {
    if (!this.data.hyperParameterTuning) {
      return data;
    }

    for (const p of this.data.hyperParameterTuning.parameters) {
      this.data.parameters = this.data.parameters.filter(
        (x) => x.name !== p.name
      );
      if (this.getHyperparameterType(p.value as string) === 'range') {
        p.value = {
          function: 'randint',
          parameters: {
            high: Number((p.value as string).split('-')[1]),
            low: Number((p.value as string).split('-')[0]),
          },
        };
      } else if (this.getHyperparameterType(p.value as string) === 'list') {
        let valueArray: any[] = (p.value as string).split(',');
        for (let v of valueArray) {
          if (!isNaN(Number(v))) {
            valueArray[valueArray.indexOf(v)] = Number(v);
          }
        }
        p.value = { values: valueArray };
      }
    }

    return data;
  }

  public getHyperparameterType(value: string): 'range' | 'list' | 'invalid' {
    if (value) {
      value = String(value);
      if (
        value.split('-').length === 2 &&
        !value.includes(',') &&
        Number(value.split('-')[0]) < Number(value.split('-')[1])
      ) {
        return 'range';
      } else if (value.split(',').length > 1 && !value.includes('-')) {
        return 'list';
      }
    }
    return 'invalid';
  }

  public isInvalid(): boolean {
    for (let parameter of this.data.parameters) {
      if (parameter.value === '' || parameter.value === null) {
        return true;
      }
    }
    if (this.data.hyperParameterTuning) {
      for (const p of this.data.hyperParameterTuning.parameters) {
        if (this.getHyperparameterType(p.value as string) === 'invalid') {
          return true;
        }
      }
    }
    return false;
  }

  public getTunableParameters(): Parameter[] {
    return this.data.parameters.filter((p) => p.type === 'int');
  }

  public notUsedAsHyperparameter(parameter: Parameter[]): Parameter[] {
    if (this.data.hyperParameterTuning) {
      return parameter.filter((p) => {
        for (const hp of this.data.hyperParameterTuning!.parameters) {
          if (p.name === hp.name) {
            return false;
          }
        }
        return true;
      });
    } else {
      return parameter;
    }
  }

  public stepHasTuning(step: Steps): boolean {
    return this.supportedSteps.includes(step);
  }

  public asBoolean(value: any): boolean {
    return value;
  }
}
