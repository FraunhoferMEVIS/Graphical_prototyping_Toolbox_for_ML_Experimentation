import { Injectable } from '@angular/core';
import { Observable, Subject, map, of } from 'rxjs';
import { UrlHelper } from '../helpers/url';
import { ModuleInstance } from '../models/network';
import { ProjectManagerApi } from '../api/project-manager/api.service';

@Injectable({
  providedIn: 'root',
})
export class DashboardService {
  public readonly TOOL_ID = 'maratus';

  private openDialogSubject: Subject<ModuleInstance> = new Subject();
  readonly openDialog$: Observable<ModuleInstance> =
    this.openDialogSubject.asObservable();

  private openPreviewDialogSubject: Subject<ModuleInstance> = new Subject();
  readonly openPreviewDialog$: Observable<ModuleInstance> =
    this.openPreviewDialogSubject.asObservable();

  private _currentProject: string = null;

  constructor(private projectManagerApi: ProjectManagerApi) {
    this._currentProject = UrlHelper.getProjectId();
  }

  public get currentProject(): string {
    return this._currentProject;
  }

  openDialog(moduleInstance: ModuleInstance) {
    this.openDialogSubject.next(moduleInstance);
  }

  openPreview(moduleInstance: ModuleInstance) {
    this.openPreviewDialogSubject.next(moduleInstance);
  }
}
