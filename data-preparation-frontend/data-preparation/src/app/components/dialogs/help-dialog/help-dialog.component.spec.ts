import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HelpDialog } from './help-dialog.component';
import {
  MAT_DIALOG_DATA,
  MatDialogModule,
  MatDialogRef,
} from '@angular/material/dialog';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { MatButtonModule } from '@angular/material/button';

describe('HelpDialogComponent', () => {
  let component: HelpDialog;
  let fixture: ComponentFixture<HelpDialog>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [HelpDialog],
      providers: [
        { provide: MatDialogRef, useValue: {} },
        {
          provide: MAT_DIALOG_DATA,
          useValue: {
            title: 'Are you sure?',
            description: 'Some description of the action.',
          },
        },
      ],
      imports: [MatDialogModule, NoopAnimationsModule, MatButtonModule],
    });
    fixture = TestBed.createComponent(HelpDialog);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
