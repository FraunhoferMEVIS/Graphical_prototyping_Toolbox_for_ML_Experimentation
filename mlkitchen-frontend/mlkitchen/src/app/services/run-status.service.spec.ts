import { TestBed } from '@angular/core/testing';

import { RunStatusService } from './run-status.service';

describe('RunStatusService', () => {
  let service: RunStatusService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RunStatusService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
