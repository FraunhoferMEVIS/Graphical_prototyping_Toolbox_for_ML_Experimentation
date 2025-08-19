import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TableComponent } from './table.component';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatTableModule } from '@angular/material/table';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { TableService } from 'src/app/services/table.service';
import { Observable, of } from 'rxjs';
import { TestData } from 'src/app/test-data';
import { TablePage } from 'src/app/api/data-preparation/api.service';
import { NotificationService } from 'src/app/services/notification.service';

class NotificationServiceMock {
  showError(message: string): void {}
  showErrorAsDialog(message: string): void {}
  showInfo(message: string): void {}
}

class TableServiceMock {
  getData(moduleId: string, page: number, size: number): Observable<TablePage> {
    return of({ columns: [], data: [] });
  }
}

describe('TableComponent', () => {
  let component: TableComponent;
  let fixture: ComponentFixture<TableComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        { provide: TableService, useClass: TableServiceMock },
        { provide: NotificationService, useClass: NotificationServiceMock },
      ],
      declarations: [TableComponent],
      imports: [NoopAnimationsModule, MatPaginatorModule, MatTableModule],
    });
    fixture = TestBed.createComponent(TableComponent);
    component = fixture.componentInstance;

    component.moduleInstance = TestData.createModuleInstance();
    component.columns = [
      {
        name: 'subject-id',
        type: 'string',
      },
      {
        name: 'hospital-flag',
        type: 'bool',
      },
    ];

    fixture.detectChanges();
  });

  it('should load table data', () => {
    expect(component).toBeTruthy();
  });
});
