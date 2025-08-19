import { Injectable } from '@angular/core';
import { Observable, of } from 'rxjs';
import { UrlHelper } from '../helpers/url';
import { DataPreparationApi } from '../api/data-preparation/api.service';

@Injectable({
  providedIn: 'root',
})
export class TableService {
  private projectId: string;

  constructor(private dataPreparationApi: DataPreparationApi) {
    this.projectId = UrlHelper.getProjectId();
  }

  getColumns(): Observable<Array<string>> {
    // TODO: get moduleId from somwhere
    // return this.networkApi.getTableColumns(this.projectId, "A");
    return of(['A', 'B']);
  }

  getData(moduleId: string, page: number, size: number) {
    return this.dataPreparationApi
      .getTable(this.projectId, moduleId, page, size)
  }
}
