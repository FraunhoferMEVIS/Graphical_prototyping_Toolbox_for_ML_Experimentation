import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CustomNodeComponent } from './custom-node.component';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { ModuleNode } from '../nodes';
import { DashboardService } from 'src/app/services/dashboard.service';
import { NetworkService } from 'src/app/services/network.service';
import { TestData } from 'src/app/test-data';
import { NotificationService } from 'src/app/services/notification.service';

class DashboardServiceMock {}

class NetworkServiceMock {}

class NotificationServiceMock {}

describe('CustomNodeComponent', () => {
  let component: CustomNodeComponent;
  let fixture: ComponentFixture<CustomNodeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [CustomNodeComponent],
      providers: [
        { provide: DashboardService, useClass: DashboardServiceMock },
        { provide: NetworkService, useClass: NetworkServiceMock },
        { provide: NotificationService, useClass: NotificationServiceMock },
      ],
      imports: [CommonModule, MatIconModule],
    }).compileComponents();

    fixture = TestBed.createComponent(CustomNodeComponent);
    component = fixture.componentInstance;
    component.data = new ModuleNode(
      'node-label',
      TestData.createModuleInstance()
    );
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
