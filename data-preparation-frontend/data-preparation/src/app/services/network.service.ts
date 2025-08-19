import { Injectable } from '@angular/core';
import {
  BehaviorSubject,
  Observable,
  Subject,
  filter,
  firstValueFrom,
  map,
  mergeMap,
  of,
} from 'rxjs';
import {
  EditorNetwork,
  ModuleInstance,
  NetworkViewModel,
  UnionValue,
} from '../models/network';
import { UrlHelper } from '../helpers/url';

import { v4 as uuid } from 'uuid';
import {
  DataPreparationApi,
  ModuleBlueprint,
  ModuleConfigOutput,
  ModuleConfigParameter,
  ModuleOutput,
} from '../api/data-preparation/api.service';

const createEmptyNetwork = () => {
  return {
    id: uuid(),
    modules: [],
    connections: [],
  };
};

/**
 * The network service has two main roles:
 *
 * 1. it offers event bus to exchange data and messages about network interactions.
 * 2. it offers functions to interact with the backend network API.
 *
 */
@Injectable({
  providedIn: 'root',
})
export class NetworkService {
  // Subjects
  private emptyNetwork = createEmptyNetwork();
  private networkSubject = new BehaviorSubject<NetworkViewModel>(
    this.emptyNetwork
  );
  private updatedModuleSubject = new Subject<ModuleOutput>();
  private modulesSubject = new BehaviorSubject<Array<ModuleBlueprint>>([]);
  private onSaveNetworkSubject = new Subject<void>();

  // Observables
  readonly network$: Observable<NetworkViewModel> =
    this.networkSubject.asObservable();
  readonly updatedModule$ = this.updatedModuleSubject.asObservable();
  readonly modules$: Observable<Array<ModuleBlueprint>> =
    this.modulesSubject.asObservable();
  readonly onSaveNetwork$: Observable<void> =
    this.onSaveNetworkSubject.asObservable();

  // The current projectId
  private projectId: string;

  constructor(private dataPreparationApi: DataPreparationApi) {
    this.projectId = UrlHelper.getProjectId();
  }

  /**
   * Fetches blueprint modules and passes them to subject.
   */
  setupModules(): Observable<void> {
    return this.dataPreparationApi.getModules().pipe(
      map((modules) => {
        this.modulesSubject.next(modules.data);
      })
    );
  }

  /**
   * Creates or gets current network each time we receive new blueprint modules.
   */
  setupNetwork(): Observable<void> {
    return this.modulesSubject.pipe(
      filter((modules) => modules.length > 0),
      mergeMap((modules) => {
        return this.dataPreparationApi.getNetwork(this.projectId).pipe(
          mergeMap((response) => {
            if (response.error && response.response.status == 404) {
              return this.dataPreparationApi
                .addNetwork(this.projectId, createEmptyNetwork())
                .pipe(map((resp) => resp.data));
            }

            return of(response.data);
          }),
          mergeMap((resp) => {
            return of({ modules: modules, network: resp });
          })
        );
      }),
      map((results) => {
        this.networkSubject.next(
          NetworkViewModel.from(results.network, results.modules)
        );
      })
    );
  }

  get network(): NetworkViewModel {
    return this.networkSubject.value;
  }

  /**
   * Create an empty network and therefore reset the current one.
   *
   * @returns observalbe indicating succces.
   */
  resetToEmptyNetwork(): Observable<boolean> {
    return this.dataPreparationApi
      .updateNetwork(this.projectId, createEmptyNetwork())
      .pipe(
        map((w) => {
          this.networkSubject.next(
            NetworkViewModel.from(w.data, this.modulesSubject.value)
          );
          return true;
        })
      );
  }

  /**
   * Emits an event that signals that the current network should be saved.
   */
  emitSaveNetworkEvent() {
    this.onSaveNetworkSubject.next();
  }

  /**
   * Save current version of network in backend.
   *
   * @param editorNetwork exported state of editor.
   * @returns
   */
  saveNetwork(editorNetwork: EditorNetwork): Observable<boolean> {
    const currentNetwork = this.networkSubject.value;
    return this.dataPreparationApi
      .addNetwork(this.projectId, {
        id: currentNetwork.id,
        modules: editorNetwork.modules,
        connections: editorNetwork.connections,
      })
      .pipe(
        map((networkOutput) => {
          // TODO update current network or just inteprete as success?
          return true;
        })
      );
  }

  /**
   * Fetches the network from the backend.
   *
   * @returns obserable with request status.
   */
  loadNetwork(): Observable<boolean> {
    return this.dataPreparationApi.getNetwork(this.projectId).pipe(
      map((w) => {
        this.networkSubject.next(
          NetworkViewModel.from(w.data, this.modulesSubject.value)
        );
        return true;
      })
    );
  }

  /**
   * Add new module to the network.
   *
   * @param module unsaved module
   * @returns promise returning the newly created instance.
   */
  addModule(module: ModuleOutput) {
    console.log('Add module: ' + module.id);

    return firstValueFrom(
      this.dataPreparationApi.addModule(this.projectId, module)
    );
  }

  /**
   * Remove a module from the network.
   *
   * @param moduleId module id.
   * @returns observable with request status.
   */
  removeModule(moduleId: string) {
    console.log('Remove module: ' + moduleId);

    return this.dataPreparationApi.deleteModule(this.projectId, moduleId);
  }

  getModuleConfig(moduleId: string): Observable<ModuleConfigOutput> {
    console.log('Get module config: ' + moduleId);

    return this.dataPreparationApi
      .getModuleConfig(this.projectId, moduleId)
      .pipe(map((r) => r.data));
  }

  runModule(moduleId: string) {
    console.log('Run module: ' + moduleId);

    return this.dataPreparationApi.executeModule(this.projectId, moduleId);
  }

  stopModule(moduleId: string): Observable<boolean> {
    console.log('Stop module: ' + moduleId);

    // return this.dataPreparationApi.stopModule(this.projectId, moduleId);
    return of(true);
  }

  runNetwork() {
    console.log('Run complete network');

    return this.dataPreparationApi.executeNetwork(this.projectId);
  }

  addConnection(
    id: string,
    sourceModule: string,
    sourceOutput: string,
    targetModule: string,
    targetInput: string
  ) {
    return this.dataPreparationApi.addConnection(this.projectId, {
      id: id,
      sourceModule: sourceModule,
      sourceSocket: sourceOutput,
      targetModule: targetModule,
      targetSocket: targetInput,
    });
  }

  removeConnection(id: string) {
    console.log('Remove connection ' + id);

    return this.dataPreparationApi.deleteConnection(this.projectId, id);
  }

  updateModule(moduleInstance: ModuleInstance) {
    console.log('Updating module ' + moduleInstance.module.id);

    let updatedModule = structuredClone(moduleInstance.module);

    return this.dataPreparationApi
      .updateModule(this.projectId, updatedModule.id, updatedModule)
      .pipe(
        map((r) => {
          if (r.response.ok) {
            this.updatedModuleSubject.next(r.data);
          }
          return r;
        })
      );
  }

  updateModuleConfig(
    moduleId: string,
    parameters: Record<string, ModuleConfigParameter>,
    updatedValues: Record<string, UnionValue>
  ) {
    for (let configKey in updatedValues) {
      // update values of the existing parameters
      parameters[configKey].value = updatedValues[configKey];
    }

    return this.dataPreparationApi.updateModuleConfig(
      this.projectId,
      moduleId,
      {
        parameters: parameters,
      }
    );
  }
}
