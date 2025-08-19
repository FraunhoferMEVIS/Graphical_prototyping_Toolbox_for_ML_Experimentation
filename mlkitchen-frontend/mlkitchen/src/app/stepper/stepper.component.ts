import { Component } from '@angular/core';
import { MethodSelectionService } from '../services/method-selection.service';
import { StepperSelectionEvent } from '@angular/cdk/stepper';
import { STEPPER_GLOBAL_OPTIONS } from '@angular/cdk/stepper';

@Component({
  selector: 'app-stepper',
  templateUrl: './stepper.component.html',
  styleUrls: ['./stepper.component.scss'],
  providers: [
    {
      provide: STEPPER_GLOBAL_OPTIONS,
      useValue: { showError: true },
    },
  ],
})
export class StepperComponent {
  showFiller = false;
  isLinear = false;

  constructor(public methodSelectionService: MethodSelectionService) {}

  public async changedStep(event: StepperSelectionEvent) {
    this.methodSelectionService.selectedStep = -1;
    await this.delay(250);
    this.methodSelectionService.selectedStep = event.selectedIndex;
  }

  private delay(ms: number) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}
