import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WorkflowDashboardComponent } from './workflow-dashboard.component';

describe('ModuleDashboardComponent', () => {
  let component: WorkflowDashboardComponent;
  let fixture: ComponentFixture<WorkflowDashboardComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [WorkflowDashboardComponent]
    });
    fixture = TestBed.createComponent(WorkflowDashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
