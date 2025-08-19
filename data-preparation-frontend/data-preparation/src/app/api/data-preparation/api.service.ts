import createClient from 'openapi-fetch';
import type { paths, components } from './schema';
import { from } from 'rxjs';
import { environment } from 'src/environments/environment';
import { Injectable } from '@angular/core';

export type ProjectPostBody = components['schemas']['ProjectPostBody'];
export type ProjectPostResponse = components['schemas']['ProjectPostResponse'];
export type TablePage = components['schemas']['TablePage'];
export type Column = components['schemas']['Column'];
export type NetworkInput = components['schemas']['Network-Input'];
export type NetworkOutput = components['schemas']['Network-Output'];
export type ModuleInput = components['schemas']['Module-Input'];
export type ModuleOutput = components['schemas']['Module-Output'];
export type ModuleConfigOutput = components['schemas']['ModuleConfig-Output'];
export type ModuleBlueprint = components['schemas']['ModuleBlueprint'];
export type ModuleConfigParameter =
  components['schemas']['ModuleConfigParameter'];
export type ModuleCategory = components['schemas']['ModuleCategory'];
export type ParameterValueType = components['schemas']['ParameterValueType'];
export type Connection = components['schemas']['Connection'];

@Injectable({
  providedIn: 'root',
})
export class DataPreparationApi {
  private client = createClient<paths>({
    baseUrl: environment.dataPreparationBasePath,
  });

  addProject(project: ProjectPostBody) {
    return from(this.client.POST('/project', { body: project, params: {} }));
  }

  getProject(projectId: string) {
    return from(
      this.client.GET('/project/{project_name}', {
        params: { path: { project_name: projectId } },
      })
    );
  }

  getModules() {
    return from(this.client.GET('/modules', { params: {} }));
  }

  updateModule(
    projectId: string,
    moduleId: string,
    updatedModule: ModuleOutput
  ) {
    return from(
      this.client.PUT('/network/{project}/module/{module_id}', {
        params: { path: { module_id: moduleId, project: projectId } },
        body: updatedModule,
      })
    );
  }

  getNetwork(projectId: string) {
    return from(
      this.client.GET('/network/{project}', {
        params: { path: { project: projectId } },
      })
    );
  }

  addNetwork(projectId: string, networkInput: NetworkInput) {
    return from(
      this.client.POST('/network/{project}', {
        params: { path: { project: projectId } },
        body: networkInput,
      })
    );
  }

  updateNetwork(projectId: string, updatedNetwork: NetworkInput) {
    return from(
      this.client.PUT('/network/{project}', {
        params: { path: { project: projectId } },
        body: updatedNetwork,
      })
    );
  }

  addConnection(projectId: string, connection: Connection) {
    return from(
      this.client.POST('/network/{project}/connection', {
        params: { path: { project: projectId } },
        body: connection,
      })
    );
  }

  deleteConnection(projectId: string, connectionId: string) {
    return from(
      this.client.DELETE('/network/{project}/connection/{connection_id}', {
        params: { path: { project: projectId, connection_id: connectionId } },
      })
    );
  }

  addModule(projectId: string, module: ModuleOutput) {
    return from(
      this.client.POST('/network/{project}/module', {
        body: module,
        params: { path: { project: projectId } },
      })
    );
  }

  deleteModule(projectId: string, moduleId: string) {
    return from(
      this.client.DELETE('/network/{project}/module/{module_id}', {
        params: { path: { project: projectId, module_id: moduleId } },
      })
    );
  }

  getModuleConfig(projectId: string, moduleId: string) {
    return from(
      this.client.GET('/network/{project}/module/{module_id}/config', {
        params: {
          path: {
            module_id: moduleId,
            project: projectId,
          },
        },
      })
    );
  }

  updateModuleConfig(projectId: string, moduleId: string, moduleConfig) {
    return from(
      this.client.PUT('/network/{project}/module/{module_id}/config', {
        body: moduleConfig,
        params: {
          path: {
            module_id: moduleId,
            project: projectId,
          },
        },
      })
    );
  }

  getVisualization(projectId: string, moduleId: string) {
    return from(
      this.client.GET('/network/{project}/module/{module_id}/visualize', {
        params: { path: { project: projectId, module_id: moduleId } },
      })
    );
  }

  getTable(projectId: string, moduleId: string, page: number, size: number) {
    return from(
      this.client.GET('/network/{project}/module/{module_id}/table', {
        params: {
          query: {
            page: page,
            size: size,
          },
          path: { project: projectId, module_id: moduleId },
        },
      })
    );
  }

  executeNetwork(projectId: string) {
    return from(
      this.client.POST('/execute/{project}', {
        params: { path: { project: projectId } },
      })
    );
  }

  executeModule(projectId: string, moduleId: string) {
    return from(
      this.client.POST('/execute/{project}/{module_id}', {
        params: { path: { project: projectId, module_id: moduleId } },
      })
    );
  }
}
