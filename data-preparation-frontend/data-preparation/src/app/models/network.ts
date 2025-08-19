import { v4 as uuid } from 'uuid';
import {
  Connection,
  ModuleBlueprint,
  ModuleOutput,
  NetworkOutput,
} from '../api/data-preparation/api.service';

/**
 * A module instance holding all required information
 * for display and interaction.
 */
export interface ModuleInstance {
  // module data from backend
  module: ModuleOutput;
  // direct access to blueprint for metadata display
  blueprint: ModuleBlueprint;

  // display data specific to frontend
  icon: string;
}

/**
 * The exported network state of the editor.
 */
export class EditorNetwork {
  modules: Array<ModuleOutput>;
  connections: Array<Connection>;
}

export class NetworkViewModel {
  id: string;
  modules: Array<ModuleInstance>;
  connections: Array<Connection>;

  constructor(
    id: string = uuid(),
    modules: Array<ModuleInstance> = Array(),
    connections: Array<Connection> = Array()
  ) {
    this.id = id;
    this.modules = modules;
    this.connections = connections;
  }

  static from(
    networkOutput: NetworkOutput,
    blueprints: Array<ModuleBlueprint>
  ): NetworkViewModel {
    // map backend responses to view model
    let moduleViews: ModuleInstance[] = networkOutput.modules.map((m) => {
      return {
        module: m,
        blueprint: blueprints.find((b) => b.id == m.blueprint),
        icon: '',
      };
    });

    let network = new NetworkViewModel(
      networkOutput.id,
      moduleViews,
      networkOutput.connections
    );

    return network;
  }
}

export type UnionValue =
  | string
  | number
  | boolean
  | string[]
  | number[]
  | boolean[]
  | null;
