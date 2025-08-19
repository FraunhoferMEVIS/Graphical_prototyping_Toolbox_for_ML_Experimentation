import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CustomSocketComponent } from './custom-socket.component';

describe('CustomSocketComponent', () => {
  let component: CustomSocketComponent;
  let fixture: ComponentFixture<CustomSocketComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CustomSocketComponent]
    });
    fixture = TestBed.createComponent(CustomSocketComponent);
    component = fixture.componentInstance;
    component.data = { name: "output" }

    fixture.detectChanges();
  });

  it('should bind name to title', () => {
    expect(component).toBeTruthy();
    expect(component.title).toBe("output")
  });
});
