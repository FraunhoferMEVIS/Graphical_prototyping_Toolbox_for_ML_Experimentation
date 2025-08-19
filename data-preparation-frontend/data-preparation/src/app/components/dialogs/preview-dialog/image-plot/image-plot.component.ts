import { Component, DestroyRef, Input, OnInit } from '@angular/core';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { ModuleInstance } from 'src/app/models/network';
import { NotificationService } from 'src/app/services/notification.service';
import { VisualizationService } from 'src/app/services/visualization.service';

@Component({
  selector: 'app-image-plot',
  templateUrl: './image-plot.component.html',
  styleUrls: ['./image-plot.component.css'],
})
export class ImagePlotComponent implements OnInit {
  @Input() moduleInstance: ModuleInstance;

  image: string;
  noData: boolean = false;
  loading: boolean = false;

  private readonly base64DataUrlPrefix = 'data:image/jpeg;base64,';

  constructor(
    private visualizationService: VisualizationService,
    private destroyRef: DestroyRef,
    private notificationService: NotificationService
  ) {}

  ngOnInit(): void {
    this.loading = true;

    this.visualizationService
      .getVisualization(this.moduleInstance.module.id)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: ({ data, error }) => {
          if (error) {
            this.noData = true;
            return;
          }

          this.image = this.base64DataUrlPrefix + data.image;
        },
        error: (error) => {
          console.error(error);

          this.noData = true;
          this.notificationService.showError(
            'Unknown error while loading image data'
          );
          this.loading = false;
        },
        complete: () => {
          this.loading = false;
        },
      });
  }
}
