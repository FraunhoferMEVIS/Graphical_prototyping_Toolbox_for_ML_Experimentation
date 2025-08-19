import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CustomConnectionComponent } from './custom-connection.component';

describe('CustomConnectionComponent', () => {
  let component: CustomConnectionComponent;
  let fixture: ComponentFixture<CustomConnectionComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CustomConnectionComponent]
    });
    fixture = TestBed.createComponent(CustomConnectionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
