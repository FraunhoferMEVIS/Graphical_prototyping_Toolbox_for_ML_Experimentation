import { TestBed } from '@angular/core/testing';

import { NetworkService } from './network.service';
import { Observable, of } from 'rxjs';
import {
  DataPreparationApi,
  NetworkOutput,
} from '../api/data-preparation/api.service';

class NetworkApiMock {
  getNetwork(projectId: string): Observable<NetworkOutput> {
    return of();
  }
}

class ModulesApiMock {
  listModulesModulesGet = () => of([]);
}

describe('NetworkService', () => {
  let service: NetworkService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [{ provide: DataPreparationApi, useClass: NetworkApiMock }],
    });
    service = TestBed.inject(NetworkService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
