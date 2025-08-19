import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CanvasComponent } from './canvas.component';
import { DashboardService } from '../../services/dashboard.service';
import { NetworkService } from 'src/app/services/network.service';
import { Observable, of } from 'rxjs';
import { ModuleInstance } from 'src/app/models/network';
import { NotificationService } from 'src/app/services/notification.service';

class DashboardServiceMock {}
class NotificationServiceMock {}
class NetworkServiceMock {
  updatedModule$: Observable<ModuleInstance> = of();
  onSaveNetwork$: Observable<void> = of();
}

describe('CanvasComponent', () => {
  let component: CanvasComponent;
  let fixture: ComponentFixture<CanvasComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        CanvasComponent,
        { provide: DashboardService, useClass: DashboardServiceMock },
        { provide: NetworkService, useClass: NetworkServiceMock },
        { provide: NotificationService, useClass: NotificationServiceMock },
      ],
    });
    fixture = TestBed.createComponent(CanvasComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
