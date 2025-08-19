import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModuleStateComponent } from './module-state.component';

describe('ModuleStatusComponent', () => {
  let component: ModuleStateComponent;
  let fixture: ComponentFixture<ModuleStateComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ModuleStateComponent]
    });
    fixture = TestBed.createComponent(ModuleStateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
