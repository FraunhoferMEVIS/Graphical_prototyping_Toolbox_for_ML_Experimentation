import { Component, Input, SimpleChanges } from '@angular/core';
import { ExecutionState } from 'src/app/workflow-dashboard/models/execution-state';

@Component({
  selector: 'module-state',
  templateUrl: './module-state.component.html',
  styleUrls: ['./module-state.component.css'],
})
export class ModuleStateComponent {
  @Input() state: ExecutionState;

  title = 'The state of this module';
  className: string;
  label: string;

  ngOnChanges(changes: SimpleChanges) {
    if (changes['state']) {
      let currentValue = changes['state'].currentValue;
      this.label = this.getStateLabel(currentValue);
      this.className = this.getStateClass(currentValue);
    }
  }

  getStateLabel(state: ExecutionState): string {
    switch (state) {
      case ExecutionState.NOT_EXECUTED: {
        return 'New';
      }
      case ExecutionState.EXECUTING: {
        return 'Executing...';
      }
      case ExecutionState.EXECUTED: {
        return 'Ready';
      }
      case ExecutionState.ERROR: {
        return 'Error';
      }
    }
  }

  getStateClass(state: ExecutionState): string {
    switch (state) {
      case ExecutionState.NOT_EXECUTED: {
        return 'not-executed';
      }
      case ExecutionState.EXECUTING: {
        return 'executing';
      }
      case ExecutionState.EXECUTED: {
        return 'executed';
      }
      case ExecutionState.ERROR: {
        return 'error';
      }
    }
  }
}
