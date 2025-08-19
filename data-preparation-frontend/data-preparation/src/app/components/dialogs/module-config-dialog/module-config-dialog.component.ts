import { Component, Inject, OnDestroy, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import {
  AbstractControl,
  FormControl,
  FormGroup,
  Validators,
} from '@angular/forms';
import { NetworkService } from '../../../services/network.service';
import { ModuleInstance, UnionValue } from 'src/app/models/network';
import { Subject, takeUntil } from 'rxjs';
import {
  ModuleConfigParameter,
  ParameterValueType,
} from 'src/app/api/data-preparation/api.service';

interface DialogData {
  moduleInstance: ModuleInstance;
}

export type InputType = 'number' | 'text';

@Component({
  selector: 'app-module-dialog',
  templateUrl: './module-config-dialog.component.html',
  styleUrls: ['./module-config-dialog.component.css'],
})
export class ModuleConfigDialogComponent implements OnInit, OnDestroy {
  private destroy$: Subject<void> = new Subject<void>();

  parameters: Array<ModuleConfigParameter> = [];
  form!: FormGroup;
  payLoad: string = '';
  error = '';

  constructor(
    public dialogRef: MatDialogRef<ModuleConfigDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: DialogData,
    private networkService: NetworkService
  ) {
    this.form = this.toFormGroup(this.parameters);
  }

  ngOnInit(): void {
    this.networkService
      .getModuleConfig(this.data.moduleInstance.module.id)
      .pipe(takeUntil(this.destroy$))
      .subscribe((config) => {
        this.parameters = Object.values(config.parameters);
        this.form = this.toFormGroup(this.parameters);
      });
  }

  ngOnDestroy(): void {
    this.destroy$.next();
    this.destroy$.complete();
  }

  onNoClick(): void {
    this.dialogRef.close();
  }

  onSubmit() {
    // raw values from form elements
    const newParameterValues: Record<string, UnionValue> =
      this.form.getRawValue();
    let parameters = this.parameters.reduce((map, obj) => {
      map[obj.id] = obj;
      return map;
    }, {});

    // Depending on the form display a number could be represented as a string.
    // Before submitting changes, we convert values back to original type.
    const convertedValues: Record<string, UnionValue> = {};
    for (let configKey in newParameterValues) {
      var value = newParameterValues[configKey];
      const param = parameters[configKey];
      if (param.multipleValues && value instanceof Array) {
        value = value.map((v: string | boolean | number) =>
          this.convertParamValue(v, param.type)
        ) as UnionValue;
      } else {
        value = this.convertParamValue(value, param.type);
      }

      convertedValues[configKey] = value;
    }

    this.networkService
      .updateModuleConfig(
        this.data.moduleInstance.module.id,
        parameters,
        convertedValues
      )
      .pipe(takeUntil(this.destroy$))
      .subscribe({
        next: ({ response }) => {
          if (response.ok) {
            this.error = '';
            this.dialogRef.close(this.payLoad);
          } else {
            this.error = 'Module update failed with status ' + response.status;
          }
        },
        error: (e) => {
          this.error = 'Request failed to complete.';
          console.error(e);
        },
      });
  }

  private toFormGroup(config: Array<ModuleConfigParameter>) {
    const group = {};

    config.forEach((p) => {
      const control = p.required
        ? new FormControl(p.value, Validators.required)
        : new FormControl(p.value);
      group[p.id] = control;
    });

    return new FormGroup(group);
  }

  getInputType(param: ModuleConfigParameter): InputType {
    if (param.type == 'float' || param.type == 'integer') {
      return 'number';
    } else {
      return 'text';
    }
  }

  /**
   * Converts passed {@param value} back to expected {@param type}.
   *
   * @param value value stored in form.
   * @param type expected type of param in the backend.
   * @returns converted value.
   */
  private convertParamValue(
    value: UnionValue,
    type: ParameterValueType
  ): UnionValue {
    if (value == null) {
      return value;
    }

    var convertedValue = value;

    switch (type) {
      case 'boolean':
        break;
      case 'integer':
        if (typeof value == 'string') {
          convertedValue = parseInt(value);
        }
        break;
      case 'float':
        if (typeof value == 'string') {
          convertedValue = parseFloat(value);
        }
        break;
      case 'string':
        break;
    }

    return convertedValue;
  }

  getInputErrorMsg(
    form: AbstractControl,
    param: ModuleConfigParameter
  ): string {
    if (form.errors && form.errors['required']) {
      if (param.multipleValues && !param.allowedValues) {
        // explicitly state that enter needs to be used so users don't wonder why input without enter
        // still throws a `required` error.
        return `${param.name} is required, press enter to add a value.`;
      } else {
        return `${param.name} is required`;
      }
    } else {
      return 'invalid value';
    }
  }

  castValueToArray(param: ModuleConfigParameter) {
    return param.value as string[];
  }

  getFormControl(id: string) {
    return this.form.get(id) as FormControl;
  }

  hasDescription(param: ModuleConfigParameter) {
    return param.description != null && param.description.trim().length > 0;
  }
}
