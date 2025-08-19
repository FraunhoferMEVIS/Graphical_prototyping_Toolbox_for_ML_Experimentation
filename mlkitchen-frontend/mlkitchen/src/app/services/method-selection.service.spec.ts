import { TestBed } from '@angular/core/testing';

import { MethodSelectionService } from './method-selection.service';

describe('MethodSelectionService', () => {
  let service: MethodSelectionService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MethodSelectionService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
