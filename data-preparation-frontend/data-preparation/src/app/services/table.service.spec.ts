import { TestBed } from '@angular/core/testing';
import { TableService } from './table.service';
import { DataPreparationApi } from '../api/data-preparation/api.service';

const mockApi = () => {}

describe('TableService', () => {
  let service: TableService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [{ provide: DataPreparationApi, useValue: mockApi}]
    });
    service = TestBed.inject(TableService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
