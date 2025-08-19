import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModuleBar } from './module-bar.component';

describe('ModuleBarComponent', () => {
  let component: ModuleBar;
  let fixture: ComponentFixture<ModuleBar>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ModuleBar]
    });
    fixture = TestBed.createComponent(ModuleBar);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
