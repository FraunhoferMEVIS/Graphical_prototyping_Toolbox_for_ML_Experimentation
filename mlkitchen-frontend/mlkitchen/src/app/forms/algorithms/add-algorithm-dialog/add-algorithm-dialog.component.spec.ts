import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AddAlgorithmDialogComponent } from './add-algorithm-dialog.component';

describe('AddAlgorithmDialogComponent', () => {
  let component: AddAlgorithmDialogComponent;
  let fixture: ComponentFixture<AddAlgorithmDialogComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AddAlgorithmDialogComponent]
    });
    fixture = TestBed.createComponent(AddAlgorithmDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
