import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AlgorithmSelectionComponent } from './algorithms.component';

describe('AlgorithmSelectionComponent', () => {
  let component: AlgorithmSelectionComponent;
  let fixture: ComponentFixture<AlgorithmSelectionComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [AlgorithmSelectionComponent],
    });
    fixture = TestBed.createComponent(AlgorithmSelectionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
