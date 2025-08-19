import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModuleConfigDialogComponent } from './module-config-dialog.component';
import { DashboardService } from '../../../services/dashboard.service';
import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { NetworkService } from 'src/app/services/network.service';
import { Observable, of } from 'rxjs';
import { TestData } from 'src/app/test-data';
import { ModuleConfigOutput } from 'src/app/api/data-preparation/api.service';

class DashboardServiceMock { }
class NetworkServiceMock {

  getModuleConfig(): Observable<ModuleConfigOutput> {
    return of({ parameters: {} })
  }
}

const dialogData = {
  moduleInstance: TestData.createModuleInstance()
}

describe('ModuleConfigDialogComponent', () => {
  let component: ModuleConfigDialogComponent;
  let fixture: ComponentFixture<ModuleConfigDialogComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ModuleConfigDialogComponent],
      providers: [
        { provide: MatDialogRef, useValue: {} },
        { provide: MAT_DIALOG_DATA, useValue: dialogData },
        { provide: DashboardService, useClass: DashboardServiceMock },
        { provide: NetworkService, useClass: NetworkServiceMock },
      ],
      imports: [
        NoopAnimationsModule,
        MatDialogModule,
        MatFormFieldModule,
        MatSelectModule,
        MatButtonModule,
        MatCheckboxModule,
        FormsModule,
        ReactiveFormsModule,
        MatInputModule
      ]
    });
    fixture = TestBed.createComponent(ModuleConfigDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
