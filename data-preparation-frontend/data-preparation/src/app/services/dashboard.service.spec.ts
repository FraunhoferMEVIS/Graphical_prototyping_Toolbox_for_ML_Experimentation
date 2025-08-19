import { TestBed } from '@angular/core/testing';

import { DashboardService } from './dashboard.service';
import { ProjectManagerApi } from '../api/project-manager/api.service';

class ProjectApiMock {}

describe('DashboardService', () => {
  let service: DashboardService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [{ provide: ProjectManagerApi, useClass: ProjectApiMock }],
    });
    service = TestBed.inject(DashboardService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
