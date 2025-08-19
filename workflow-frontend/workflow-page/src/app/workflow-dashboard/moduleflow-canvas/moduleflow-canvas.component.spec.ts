import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModuleflowCanvasComponent } from './moduleflow-canvas.component';

describe('ModuleflowCanvasComponent', () => {
  let component: ModuleflowCanvasComponent;
  let fixture: ComponentFixture<ModuleflowCanvasComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ModuleflowCanvasComponent]
    });
    fixture = TestBed.createComponent(ModuleflowCanvasComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
