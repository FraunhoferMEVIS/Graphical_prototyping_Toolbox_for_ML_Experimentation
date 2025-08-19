import { Component, Input, Output, EventEmitter } from '@angular/core';
import { Observable, BehaviorSubject } from 'rxjs';
import { Method } from 'src/app/models/method';
@Component({
  selector: 'app-selected-options',
  templateUrl: './selected-options.component.html',
  styleUrls: ['./selected-options.component.scss'],
})
export class SelectedOptionsComponent {
  @Input() formName: string = '';
  @Input() options: Method[] = [];
  @Output() optionsEmitter: EventEmitter<Method[]> = new EventEmitter<
    Method[]
  >();
  constructor() {}

  public deselectOption(option: Method) {
    let op = this.options.filter((o) => o !== option);
    this.optionsEmitter.emit(op);
  }

  public toMethodSetting(settingName: string, value): string | null {
    if (value != undefined && value != null) {
      return settingName + ': ' + JSON.stringify(value);
    }
    return null;
  }

  public getParameters(parameters: Object): string[] {
    if (parameters == undefined) {
      return [];
    }
    return Object.keys(parameters).filter(
      (p) =>
        p !== 'search_space' && p !== 'hyper_parameter_tuning' && p !== 'n_iter'
    );
  }

  public hasHyperparametertuning(parameters: Object): boolean {
    if (parameters == undefined) {
      return false;
    }
    return (
      parameters['search_space'] &&
      Object.keys(parameters['search_space']).length > 0
    );
  }
}
