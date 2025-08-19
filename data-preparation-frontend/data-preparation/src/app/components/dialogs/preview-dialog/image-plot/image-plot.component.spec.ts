import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ImagePlotComponent } from './image-plot.component';
import { VisualizationService } from 'src/app/services/visualization.service';
import { of } from 'rxjs';
import { TestData } from 'src/app/test-data';
import { NotificationService } from 'src/app/services/notification.service';

class VisualizationServiceMock {
  getVisualization(moduleId: string) {
    return of({ image: 'asdfasdf' });
  }
}

class NotificationServiceMock {}

describe('ImagePlotComponent', () => {
  let component: ImagePlotComponent;
  let fixture: ComponentFixture<ImagePlotComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        { provide: VisualizationService, useClass: VisualizationServiceMock },
        { provide: NotificationService, useClass: NotificationServiceMock },
      ],
      declarations: [ImagePlotComponent],
    });
    fixture = TestBed.createComponent(ImagePlotComponent);
    component = fixture.componentInstance;
    component.moduleInstance = TestData.createModuleInstance();
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
