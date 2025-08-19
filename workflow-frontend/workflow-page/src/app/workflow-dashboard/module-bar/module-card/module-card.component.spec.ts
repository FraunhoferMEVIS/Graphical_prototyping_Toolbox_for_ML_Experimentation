import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModuleCard } from './module-card.component';

describe('ModuleCard', () => {
  let component: ModuleCard;
  let fixture: ComponentFixture<ModuleCard>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ModuleCard]
    });
    fixture = TestBed.createComponent(ModuleCard);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
