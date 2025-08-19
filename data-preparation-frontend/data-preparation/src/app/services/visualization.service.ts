import { Injectable } from '@angular/core';
import { UrlHelper } from '../helpers/url';
import { DataPreparationApi } from '../api/data-preparation/api.service';

@Injectable({
  providedIn: 'root',
})
export class VisualizationService {
  private projectId: string;

  constructor(private dataPreparationApi: DataPreparationApi) {
    this.projectId = UrlHelper.getProjectId();
  }

  getVisualization(moduleId: string) {
    return this.dataPreparationApi.getVisualization(this.projectId, moduleId);
  }
}
