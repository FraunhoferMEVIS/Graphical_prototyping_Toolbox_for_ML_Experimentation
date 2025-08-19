import { ModuleOutput } from './models/module-output';
import {
  ModuleIOFlowList,
  ModuleIOFlow,
  ModuleInstances,
} from './workflow-dashboard.model';
import { ModuleInstance } from './models/module-instance';
import {
  BASIC_WORKFLOW_TEMPLATE,
  MODULES,
} from './workflow-dashboard.config';
import { Injectable } from '@angular/core';
import {
  BehaviorSubject,
  Observable,
  Subject,
  filter,
  forkJoin,
  map,
  mergeMap,
  of,
  timer,
} from 'rxjs';
import { Workflow } from './models/workflow';
import { Module } from './models/module';
import { DefaultService, ProjectsService } from '../api/project-manager';
import { ExecutionState } from './models/execution-state';
import { UrlHelper } from '../helpers/url-helper';
import { Location } from '@angular/common';
import { WorkflowTemplate } from './models/workflow-template';
import Cookies from 'js-cookie';
import {
  HttpClient,
  HttpErrorResponse,
  HttpHeaders,
} from '@angular/common/http';
import { environment } from 'src/environments/environment';
import { compilePipeFromMetadata } from '@angular/compiler';

const TEMPLATE_KEY = 'template-selection';
type TEMPLATE = 'basic' | null;

@Injectable({ providedIn: 'root' })
export class DashboardService {
  public userName$: Observable<string>;
  private workflowSubject: BehaviorSubject<Workflow> = new BehaviorSubject(BASIC_WORKFLOW_TEMPLATE.workflow
  );
  readonly workflow$: Observable<Workflow> =
    this.workflowSubject.asObservable();

  private modulesSubject: BehaviorSubject<Array<Module>> = new BehaviorSubject(
    MODULES
  );
  readonly modules$: Observable<Array<Module>> =
    this.modulesSubject.asObservable();

  private projectsSubject = new BehaviorSubject<string[]>([]);
  readonly projects$: Observable<string[]> =
    this.projectsSubject.asObservable();

  private selectedProjectSubject: BehaviorSubject<string> =
    new BehaviorSubject<string>(null);
  readonly selectedProject$: Observable<string> =
    this.selectedProjectSubject.asObservable();

  private updatedModulesSubject: Subject<void> = new Subject();
  readonly updatedModules$ = this.updatedModulesSubject.asObservable();

  constructor(
    private location: Location,
    private projectsService: ProjectsService,
    private defaultService: DefaultService,
    private httpClient: HttpClient
  ) {
    // fetch & update every x seconds the progress state of each module loaded in the workflow.
    timer(0, 2000)
      .pipe(
        filter(() => this.selectedProjectSubject.value != null),
        mergeMap(() => {
          let currentWorkflow = this.workflowSubject.value;
          return forkJoin(
            currentWorkflow.moduleInstances.map((m) =>
              this.updateProgressOfModule(m)
            )
          );
        })
      )
      .subscribe(() => {
        // derive inputs
        let currentWorkflow = this.workflowSubject.value;
        currentWorkflow.moduleInstances.forEach((m) => {
          let input = this.getModuleInputData(
            m.id,
            currentWorkflow.moduleInstances,
            currentWorkflow.connections
          );
          m.data.in = input;
        });

        // explictily update node components so that they re-render based on modified moduleInstance.
        this.updatedModulesSubject.next();
      });
  }

  private updateProgressOfModule(moduleInstance: ModuleInstance) {
    return this.defaultService
      .getProgressApiProgressProjectIdToolIdGet(
        this.selectedProjectSubject.value,
        moduleInstance.module.id
      )
      .pipe(
        map((r) => {
          let status = r['status'];

          switch (status) {
            case 'finished': {
              moduleInstance.state = ExecutionState.EXECUTED;

              // add dummy export
              moduleInstance.data.out = [
                {
                  id: moduleInstance.module.id,
                  timestamp: 'asd',
                  moduleId: moduleInstance.module.id,
                  meta: {
                    label: 'yeah',
                  },
                },
              ];

              break;
            }
            case 'unused': {
              moduleInstance.state = ExecutionState.NOT_EXECUTED;
              moduleInstance.data.out = [];
              break;
            }
            case 'in_progress': {
              moduleInstance.state = ExecutionState.EXECUTING;
              break;
            }
            default: {
              moduleInstance.state = ExecutionState.NOT_EXECUTED;
              moduleInstance.data.out = [];
              break;
            }
          }
        })
      );
  }

  deleteProject(project: string) {
    return this.projectsService.deleteProjectProjectsProjectIdDelete(project);
  }

  renameProject(project: string, newProject: string) {
    return this.projectsService.updateProjectProjectsProjectIdPut(project, {
      id: newProject,
    });
  }

  loadProjects(): Observable<string[]> {
    return this.projectsService.getProjectsProjectsGet().pipe(
      map((projects) => projects.sort()),
      map((projects) => {
        this.projectsSubject.next(projects);
        return projects;
      })
    );
  }

  selectProject(project: string) {
    const params = UrlHelper.updateParameter(project);
    this.location.go('/', params);

    this.selectedProjectSubject.next(project);
  }

  getProjectFromPath(): string {
    return UrlHelper.getProjectId();
  }

  newWorkflow() {
    let w = new Workflow();
    this.workflowSubject.next(w);
  }

  createProject(projectName: string): Observable<boolean> {
    return this.projectsService.createProjectProjectsPost({
      id: projectName
    });
  }

  loadWorkflow(template: WorkflowTemplate = BASIC_WORKFLOW_TEMPLATE) {
    this.persistTemplateSelection(
      template == BASIC_WORKFLOW_TEMPLATE ? 'basic' : null
    );
    this.workflowSubject.next(template.workflow);
  }

  getModuleInputData(
    moduleId: string,
    modules: ModuleInstances,
    moduleDataFlows: ModuleIOFlowList
  ): Array<ModuleOutput> {
    let dataSourceIds: String[] = this.getDataSourceIds(
      moduleId,
      moduleDataFlows
    );
    return this.getConnectedOutputData(dataSourceIds, modules);
  }

  getConnectedOutputData(
    dataSourceIds: String[],
    modules: ModuleInstances
  ): Array<ModuleOutput> {
    let result: Array<ModuleOutput> = [];
    modules.forEach((m: ModuleInstance) => {
      if (dataSourceIds.includes(m.id)) {
        result = result.concat(m.data.out);
      }
    });
    return result;
  }

  getDataSourceIds(
    moduleId: string,
    moduleIOFlows: ModuleIOFlowList
  ): Array<String> {
    let result: String[] = [];
    moduleIOFlows.forEach((flow: ModuleIOFlow) => {
      if (flow.to === moduleId) {
        result.push(flow.from);
      }
    });
    return result;
  }

  /**
   * Read template selection from cookie.
   */
  private readTemplateSelection() {
    return Cookies.get(TEMPLATE_KEY) as TEMPLATE;
  }

  /**
   * Persists template selection as cookie.
   */
  private persistTemplateSelection(template: TEMPLATE) {
    Cookies.set(TEMPLATE_KEY, template.toString());
  }
}
