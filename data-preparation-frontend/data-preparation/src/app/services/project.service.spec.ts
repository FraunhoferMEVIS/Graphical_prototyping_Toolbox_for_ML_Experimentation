import { TestBed } from '@angular/core/testing';
import { ProjectService } from './project.service';
import { DataPreparationApi } from '../api/data-preparation/api.service';

class ProjectApiMock {
}

describe('ProjectService', () => {
  let service: ProjectService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [{ provide: DataPreparationApi, useClass: ProjectApiMock }],
    });
    service = TestBed.inject(ProjectService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
