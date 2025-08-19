import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ManageProjectDialogComponent } from './manage-project-dialog.component';

describe('ManageProjectDialogComponent', () => {
  let component: ManageProjectDialogComponent;
  let fixture: ComponentFixture<ManageProjectDialogComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ManageProjectDialogComponent],
    });
    fixture = TestBed.createComponent(ManageProjectDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
