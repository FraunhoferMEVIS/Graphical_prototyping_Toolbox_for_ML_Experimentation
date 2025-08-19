import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WorkflowModuleIOComponent } from './workflow-module-io.component';

describe('WorkflowModuleIOComponent', () => {
  let component: WorkflowModuleIOComponent;
  let fixture: ComponentFixture<WorkflowModuleIOComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [WorkflowModuleIOComponent]
    });
    fixture = TestBed.createComponent(WorkflowModuleIOComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
