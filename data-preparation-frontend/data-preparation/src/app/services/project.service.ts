import { Injectable } from '@angular/core';
import { UrlHelper } from '../helpers/url';
import { Subject, map, mergeMap, of } from 'rxjs';
import { DataPreparationApi } from '../api/data-preparation/api.service';

export interface Project {
  name: string;
}

@Injectable({
  providedIn: 'root',
})
export class ProjectService {
  private projectId: string;

  private projectSubject = new Subject<Project>();
  public readonly project$ = this.projectSubject.asObservable();

  constructor(private dataPreparationApi: DataPreparationApi) {
    this.projectId = UrlHelper.getProjectId();
  }

  getOrCreateProject() {
    return this.getProject().pipe(
      mergeMap((r) => {
        if (r.response.status == 404) {
          return this.createProject().pipe(
            map(({ data }) => {
              this.projectSubject.next({ name: this.projectId });
              return data;
            })
          );
        } else {
          const project = r.data;
          this.projectSubject.next(project);
          return of(project);
        }
      })
    );
  }

  createProject() {
    return this.dataPreparationApi.addProject({
      name: this.projectId,
    });
  }

  getProject() {
    return this.dataPreparationApi.getProject(this.projectId);
  }
}
