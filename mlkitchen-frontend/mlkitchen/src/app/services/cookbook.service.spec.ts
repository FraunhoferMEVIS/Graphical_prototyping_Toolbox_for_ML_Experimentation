import { TestBed } from '@angular/core/testing';

import { CookbookService } from './cookbook.service';

describe('CookbookService', () => {
  let service: CookbookService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CookbookService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
