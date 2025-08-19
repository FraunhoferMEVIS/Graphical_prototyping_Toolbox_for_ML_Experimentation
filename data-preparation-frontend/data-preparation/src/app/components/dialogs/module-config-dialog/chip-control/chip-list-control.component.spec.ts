import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ChipListControlComponent } from './chip-list-control.component';
import { MatChipsModule } from '@angular/material/chips';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { FormControl, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { MatIconModule } from '@angular/material/icon';

describe('ChipControlComponent', () => {
  let component: ChipListControlComponent;
  let fixture: ComponentFixture<ChipListControlComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ChipListControlComponent],
      imports: [
        NoopAnimationsModule,
        MatChipsModule,
        MatFormFieldModule,
        MatInputModule,
        ReactiveFormsModule,
        FormsModule,
        MatIconModule,
      ],
    });
    fixture = TestBed.createComponent(ChipListControlComponent);
    component = fixture.componentInstance;
    component.control = new FormControl([]);
    component.values = ['A', 'B'];
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
