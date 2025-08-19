import { waitForAsync, ComponentFixture, TestBed } from '@angular/core/testing';
import { NoopAnimationsModule } from '@angular/platform-browser/animations';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { MatListModule } from '@angular/material/list';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatToolbarModule } from '@angular/material/toolbar';

import { DashboardComponent } from './dashboard.component';
import { DashboardService } from '../../services/dashboard.service';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { MatMenuModule } from '@angular/material/menu';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { Component, Input } from '@angular/core';
import { Observable, of } from 'rxjs';
import { NetworkViewModel } from '../../models/network';
import { ModulesListComponent } from './modules-list/modules-list.component';
import { MatTooltipModule } from '@angular/material/tooltip';
import { NetworkService } from 'src/app/services/network.service';
import { Project, ProjectService } from 'src/app/services/project.service';
import { ModuleBlueprint } from 'src/app/api/data-preparation/api.service';
import { ModulesListNestedComponent } from './modules-list-nested/modules-list-nested.component';

class NetworkServiceMock {
  modules$ = of([]);
  network$ = of();

  setupNetwork(): Observable<void> {
    return of();
  }
}

class ProjectServiceMock {
  project$ = of({ name: 'my-project' });

  getOrCreateProject(): Observable<Project> {
    return of({ name: 'my-project' });
  }
}

class DashboardServiceMock {
  currentProject = 'My-Project';

  network$ = of({});
  modules$ = of([]);

  openDialog$ = of();
  openPreviewDialog$ = of();
}

@Component({ standalone: true, selector: 'app-canvas', template: '' })
class AppCanvasMock {
  @Input() network: NetworkViewModel;
  @Input() modules: Array<ModuleBlueprint>;
}

describe('DashboardComponent', () => {
  let component: DashboardComponent;
  let fixture: ComponentFixture<DashboardComponent>;

  beforeEach(waitForAsync(() => {
    TestBed.configureTestingModule({
      declarations: [DashboardComponent, ModulesListComponent, ModulesListNestedComponent],
      providers: [
        { provide: DashboardService, useClass: DashboardServiceMock },
        { provide: NetworkService, useClass: NetworkServiceMock },
        { provide: ProjectService, useClass: ProjectServiceMock },
        { provide: MatDialog, useValue: {} },
        { provide: MatSnackBar, useValue: {} },
      ],
      imports: [
        MatMenuModule,
        NoopAnimationsModule,
        MatButtonModule,
        MatIconModule,
        MatListModule,
        MatSidenavModule,
        MatToolbarModule,
        FormsModule,
        MatFormFieldModule,
        MatDialogModule,
        AppCanvasMock,
        MatTooltipModule,
        MatIconModule,
      ],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DashboardComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should compile', () => {
    expect(component).toBeTruthy();
  });
});
