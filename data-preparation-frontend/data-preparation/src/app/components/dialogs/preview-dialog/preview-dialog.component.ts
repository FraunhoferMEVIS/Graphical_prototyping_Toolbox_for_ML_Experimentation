import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogRef } from '@angular/material/dialog';
import { ModuleInstance } from 'src/app/models/network';

export interface DialogData {
  moduleInstance: ModuleInstance;
}

@Component({
  selector: 'app-preview-dialog',
  templateUrl: './preview-dialog.component.html',
  styleUrls: ['./preview-dialog.component.css'],
})
export class PreviewDialogComponent {
  constructor(
    public dialogRef: MatDialogRef<PreviewDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public readonly data: DialogData
  ) {}

  getTitle(moduleInstance: ModuleInstance) {
    if (moduleInstance.blueprint.category == 'Visualize') {
      return `Visualization of '${moduleInstance.module.label}'`;
    } else {
      return `Table data of '${moduleInstance.module.label}'`;
    }
  }
}
