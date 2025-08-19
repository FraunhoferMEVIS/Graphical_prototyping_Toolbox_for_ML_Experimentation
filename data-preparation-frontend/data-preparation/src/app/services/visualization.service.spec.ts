import { TestBed } from '@angular/core/testing';
import { VisualizationService } from './visualization.service';
import { DataPreparationApi } from '../api/data-preparation/api.service';

const mockApi = () => { }

describe('VisualizationService', () => {
  let service: VisualizationService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [{ provide: DataPreparationApi, useValue: mockApi }]
    });
    service = TestBed.inject(VisualizationService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
