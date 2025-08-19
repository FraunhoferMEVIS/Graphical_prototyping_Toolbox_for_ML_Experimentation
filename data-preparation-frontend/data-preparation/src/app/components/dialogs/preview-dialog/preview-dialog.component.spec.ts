import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PreviewDialogComponent } from './preview-dialog.component';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { CommonModule, NgSwitchCase } from '@angular/common';
import { Component, Input } from '@angular/core';
import { ModuleInstance } from 'src/app/models/network';
import { TestData } from 'src/app/test-data';


@Component({ standalone: true, selector: "app-table", template: "" })
class AppTableMock {
  @Input() moduleInstance: ModuleInstance;
}

describe('PreviewDialogComponent', () => {
  let component: PreviewDialogComponent;
  let fixture: ComponentFixture<PreviewDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [PreviewDialogComponent],
      providers: [
        { provide: MatDialogRef, useValue: {} },
        { provide: MAT_DIALOG_DATA, useValue: { moduleInstance: TestData.createModuleInstance() } }
      ],
      imports: [CommonModule, NgSwitchCase, AppTableMock]
    }).compileComponents();
    fixture = TestBed.createComponent(PreviewDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
