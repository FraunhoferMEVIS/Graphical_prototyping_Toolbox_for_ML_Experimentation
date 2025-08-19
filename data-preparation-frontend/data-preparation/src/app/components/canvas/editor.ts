import { Injector } from '@angular/core';
import { NodeEditor, GetSchemes, ClassicPreset } from 'rete';
import { AreaPlugin, AreaExtensions } from 'rete-area-plugin';
import {
  ConnectionPlugin,
  Presets as ConnectionPresets,
} from 'rete-connection-plugin';
import { AngularPlugin, AngularArea2D, Presets } from 'rete-angular-plugin/16';
import { CustomNodeComponent } from './custom-node/custom-node.component';
import {
  ButtonComponent,
  ButtonControl,
} from './controls/custom-button.component';
import { CustomConnectionComponent } from './custom-connection/custom-connection.component';
import { CustomSocketComponent } from './custom-socket/custom-socket.component';
import { ModuleNode, Node } from './nodes';
import {
  AutoArrangePlugin,
  Presets as ArrangePresets,
} from 'rete-auto-arrange-plugin';
import {
  EditorNetwork as EditorNetwork,
  ModuleInstance,
  NetworkViewModel,
} from '../../models/network';
import { ItemDefinition } from 'rete-context-menu-plugin/_types/presets/classic/types';
import {
  ContextMenuExtra,
  ContextMenuPlugin,
  Presets as ContextMenuPresets,
} from 'rete-context-menu-plugin';
import { Subject } from 'rxjs';
import { NetworkService } from '../../services/network.service';
import { NodeFactory } from './node-factory';
import { v4 as uuid } from 'uuid';
import {
  ModuleBlueprint,
  ModuleOutput,
} from 'src/app/api/data-preparation/api.service';
import { toPriority } from 'src/app/models/category';

export enum EventType {
  ERROR,
}

export interface EditorEvent {
  type: EventType;
  message: string;
  data?: any;
}

class Connection<N extends Node> extends ClassicPreset.Connection<N, N> {}
type Schemes = GetSchemes<Node, Connection<Node>>;
type AreaExtra = AngularArea2D<Schemes> | ContextMenuExtra;

type NodeMap = {
  [key: string]: Node;
};

const MESSAGES = {
  ONE_EXPORT_MODULE: 'Only one export module can exist in a network',
};

const EXPORT_MODULE_ID = 'export';

/**
 * A wrapper of three.js, offering a high-level interface to manage the network visualization.
 */
export class Editor {
  private editor: NodeEditor<Schemes>;
  private area: AreaPlugin<Schemes, AreaExtra>;
  private arrange: AutoArrangePlugin<Schemes>;

  private networkService: NetworkService;

  private eventSubject = new Subject<EditorEvent>();
  public readonly events$ = this.eventSubject.asObservable();

  // Tracks whether editor is in the middle of clearing state.
  private clearing = false;

  private nodeConnectionPreset = Presets.classic.setup({
    customize: {
      node() {
        return CustomNodeComponent;
      },
      control(data) {
        if (data.payload instanceof ButtonControl) {
          return ButtonComponent;
        }

        return null;
      },
      connection() {
        return CustomConnectionComponent;
      },
      socket() {
        return CustomSocketComponent;
      },
    },
  });

  constructor(container: HTMLElement, injector: Injector) {
    const editor = new NodeEditor<Schemes>();
    const area = new AreaPlugin<Schemes, AreaExtra>(container);
    const connection = new ConnectionPlugin<Schemes, AreaExtra>();
    const render = new AngularPlugin<Schemes, AreaExtra>({ injector });
    const arrange = new AutoArrangePlugin<Schemes>();

    this.networkService = injector.get(NetworkService);

    this.arrange = arrange;
    this.area = area;
    this.editor = editor;

    AreaExtensions.selectableNodes(area, AreaExtensions.selector(), {
      // disable accumulating until we properly support it
      accumulating: {
        active() {
          return false;
        },
      },
    });

    arrange.addPreset(ArrangePresets.classic.setup());
    area.use(arrange);

    render.addPreset(Presets.contextMenu.setup({ delay: 0 }));
    render.addPreset(this.nodeConnectionPreset);

    render.addPreset(Presets.classic.setup());
    connection.addPreset(ConnectionPresets.classic.setup());

    /**
     * Register to area events.
     */
    area.addPipe((context) => {
      if (context.type == 'nodedragged') {
        // in contrast to "nodetranslated" this fires only once
        // when dragging ends => we get the final x/y position of a node.
        let moduleNode = context.data as ModuleNode;
        let nodeView = this.area.nodeViews.get(context.data.id);

        const previousPosition = moduleNode.moduleInstance.module.position;
        if (
          previousPosition.x == nodeView.position.x &&
          previousPosition.y == nodeView.position.y
        ) {
          // skip update if position didn't change
          return context;
        }

        moduleNode.moduleInstance.module.position = nodeView.position;

        this.networkService.updateModule(moduleNode.moduleInstance).subscribe({
          next: ({ response }) => {
            if (!response.ok) {
              this.sendErrorEvent(
                'Module update rejected with code: ' + response.status
              );
            }
          },
          error: (_) =>
            this.sendErrorEvent(
              'Failed to update module due to network|backend error'
            ),
        });
      } else if (context.type == 'nodetranslated') {
        // TODO: update here x/y position at least in moduleInstance.modul to support multi-selection dragging?
      }

      return context;
    });

    /**
     * Register here to editor events (e.g. node|connection created|removed)
     *
     * Returning with null stops propagation of an event.
     *
     * https://retejs.org/docs/guides/validation#validation
     */
    editor.addPipe((context) => {
      if (context.type == 'nodecreate') {
        // before node is added, e.g. verify that node is valid

        const node = context.data as ModuleNode;
        if (
          node.moduleInstance.blueprint.id == EXPORT_MODULE_ID &&
          this.anyExportModuleWithDifferentId(node.id)
        ) {
          this.sendErrorEvent(MESSAGES.ONE_EXPORT_MODULE);
          return undefined;
        }
      }

      if (context.type == 'nodecreated') {
        // ignore, already done in context menu
      }

      if (context.type == 'connectioncreated') {
        // ignore
      }

      if (context.type == 'noderemoved') {
        if (!this.clearing) {
          this.networkService.removeModule(context.data.id).subscribe({
            next: ({ response }) => {
              if (!response.ok) {
                this.sendErrorEvent(
                  'Failed to remove node: ' + response.status
                );
              }
            },
            error: (_) => {
              this.sendErrorEvent(
                'Failed to remove node due to network|backend error'
              );
            },
          });
        }
      }

      if (context.type == 'connectionremove') {
        if (!this.clearing) {
          this.networkService.removeConnection(context.data.id).subscribe({
            next: ({ response }) => {
              if (response.status == 404) {
                // ignore silently since backend might already removed this connection
                // as part of deleting a module
                return;
              }

              if (!response.ok) {
                this.sendErrorEvent(
                  'Failed to remove connection: ' + response.status
                );
              }
            },
            error: (_) => {
              this.sendErrorEvent(
                'Failed to remove connection due to network|backend error'
              );
            },
          });
        }
      }

      if (context.type == 'cleared') {
        this.clearing = false;
        console.debug('cleared');
      }

      if (context.type == 'clear') {
        this.clearing = true;
        console.debug('clear');
      }

      if (context.type == 'clearcancelled') {
        this.clearing = false;
        console.debug('clear cancelled');
      }

      if (context.type == 'connectioncreate') {
        if (!this.clearing) {
          // verify if this is a valid connection
          const sourceNode = this.editor.getNode(
            context.data.source
          ) as ModuleNode;
          const targetNode = this.editor.getNode(
            context.data.target
          ) as ModuleNode;

          const sourceOutput = context.data.sourceOutput;
          const targetInput = context.data.targetInput;

          // verify if connection already exists in state
          let alreadyExists = this.networkService.network.connections.find(
            (c) =>
              c.sourceModule == sourceNode.id &&
              c.targetModule == targetNode.id &&
              c.sourceSocket == sourceOutput &&
              c.targetSocket == targetInput
          );
          if (alreadyExists) {
            // skip backend call
            return context;
          }

          if (!this.isConnectionValid(sourceNode, targetNode)) {
            return undefined;
          }

          this.networkService
            .addConnection(
              context.data.id,
              sourceNode.id,
              sourceOutput,
              targetNode.id,
              targetInput
            )
            .subscribe({
              next: ({ response }) => {
                if (!response.ok) {
                  this.sendErrorEvent(
                    'Connection was rejected with status: ' + response.status
                  );
                }
              },
              error: (_) => {
                this.sendErrorEvent(
                  'Failed to add connection due to network|backend error'
                );

                this.editor.emit({ type: 'clear' });
                this.editor.removeConnection(context.data.id);
                this.editor.emit({ type: 'cleared' });
              },
            });
        }

        return context;
      }

      return context;
    });

    editor.use(area);
    area.use(connection);
    area.use(render);

    AreaExtensions.simpleNodesOrder(area);
  }

  /**
   * Tests whether an export module with another id is already present in the network.
   *
   * @returns true if exists.
   */
  private anyExportModuleWithDifferentId(id: string) {
    return this.editor.getNodes().some((n) => {
      const existingNode = n as ModuleNode;
      return (
        existingNode.moduleInstance.blueprint.id == EXPORT_MODULE_ID &&
        existingNode.id != id
      );
    });
  }

  /**
   * Validates a connection by verifying some common rules before the connection is created.
   *
   * @param sourceNode source node.
   * @param targetNode target node.
   * @returns true if valid else false
   */
  private isConnectionValid(sourceNode: ModuleNode, targetNode: ModuleNode) {
    if (sourceNode.id == targetNode.id) {
      this.sendErrorEvent('A module cannot connect to itself');
      return false;
    }

    return true;
  }

  /**
   * Triggers an update of all node components in the canvas.
   *
   * Node components will re-render on update.
   */
  async updateNodes() {
    for (let n of this.editor.getNodes()) {
      await this.area.update('node', n.id);
    }
  }

  /**
   * Add a module to the canvas.
   *
   * @param moduleBlueprint blueprint for module creation.
   */
  async addModule(moduleBlueprint: ModuleBlueprint) {
    let instance = createModuleInstance(moduleBlueprint);
    let node = NodeFactory.createModuleNode(instance);

    await this.editor.addNode(node);
    await this.area.translate(node.id, this.area.area.pointer);

    // update position
    instance.module.position = this.area.area.pointer;

    if (
      !(
        moduleBlueprint.id == EXPORT_MODULE_ID &&
        this.anyExportModuleWithDifferentId(node.id)
      )
    ) {
      // create module in backend
      this.networkService
        .addModule(instance.module)
        .then(({ response, data }) => {
          if (!response.ok) {
            throw Error('rejected');
          }

          return this.addSockets(node, data);
        })
        .then()
        .catch((rejected) => {
          this.editor.emit({ type: 'clear' });
          this.sendErrorEvent('Node was rejected ' + rejected.message);
          return this.editor.removeNode(node.id);
        })
        .then(() => {
          this.editor.emit({ type: 'cleared' });
        });
    }

    return () => this.area.destroy();
  }

  /**
   * Update a single ModuleNode node, causing the underlying component to re-render.
   *
   * @param id of moduleInstance
   * @param moduleInstance updated instance
   */
  async updateNode(id: string, moduleOutput: ModuleOutput) {
    var node = this.editor.getNode(id) as ModuleNode;
    if (!node) {
      return;
    }

    node.moduleInstance.module = moduleOutput;
    await this.area.update('node', node.id);
  }

  /**
   * Create a rete.js graph based on {@param network}.
   *
   * @param network
   */
  async import(network: NetworkViewModel) {
    // make sure we start on empty canvas.
    await this.editor.clear();

    var nodeMap: NodeMap = {};

    // (1) create the nodes and store them in a map
    const nodePromises = network.modules.map((moduleInstance) => {
      const node: Node = NodeFactory.createModuleNode(moduleInstance);
      nodeMap[moduleInstance.module.id] = node;

      return this.editor
        .addNode(node)
        .then(() =>
          this.area.translate(node.id, moduleInstance.module.position)
        );
    });
    await Promise.all(nodePromises);

    // (2) create connections by accessing node map
    const connectionPromises = network.connections.map((connection) => {
      let outputNode = nodeMap[connection.sourceModule];
      let inputNode = nodeMap[connection.targetModule];

      let conn = new Connection(
        outputNode,
        connection.sourceSocket,
        inputNode,
        connection.targetSocket
      );
      conn.id = connection.id;
      return this.editor.addConnection(conn);
    });
    await Promise.all(connectionPromises);

    // focus area on graph
    await AreaExtensions.zoomAt(this.area, this.editor.getNodes());

    return () => this.area.destroy();
  }

  /**
   * Adds the input and output sockets to a node
   * when receiving the created {@param module} from backend.
   *
   * @param node existing node in editor.
   * @param module created module in the backend.
   * @returns promise that updates node.
   */
  private addSockets(node: ModuleNode, module: ModuleOutput) {
    // TODO: remove when we have the inputs/outputs as part of the blueprint
    const socket = new ClassicPreset.Socket('socket');
    node.moduleInstance.module = module;
    node.moduleInstance.module.output_sockets.forEach((output) => {
      node.addOutput(
        output.name,
        new ClassicPreset.Output(socket, output.name)
      );
    });

    node.moduleInstance.module.input_sockets.forEach((input) => {
      node.addInput(
        input.name,
        new ClassicPreset.Input(socket, input.name, NodeFactory.MULTIPLE_INPUTS)
      );
    });

    return this.updateNode(node.id, node.moduleInstance.module);
  }

  /**
   * Refreshes context menu items with {@param modules}.
   *
   * @param modules most recent modules.
   */
  populateMenu(modules: Array<ModuleBlueprint>) {
    if (modules == null) {
      return;
    }

    const groupedModules = this.groupByCategory(modules);
    const sortedKeys = Array.from(groupedModules.keys()).sort((a, b) => {
      return toPriority(a) - toPriority(b);
    });

    let menuItems: ItemDefinition<Schemes>[] = sortedKeys.map((m) => [
      m,
      groupedModules.get(m).map((m) => [
        m.title,
        () => {
          let instance = createModuleInstance(m);
          // set target position that the contextMenu impl uses
          instance.module.position = this.area.area.pointer;

          let node = NodeFactory.createModuleNode(instance);

          if (
            !(
              m.id == EXPORT_MODULE_ID &&
              this.anyExportModuleWithDifferentId(node.id)
            )
          ) {
            this.networkService
              .addModule(instance.module)
              .then(({ response, data }) => {
                if (!response.ok) {
                  this.sendErrorEvent(
                    'Node was rejected with code: ' + response.status
                  );
                  throw Error('Reject');
                }

                return this.addSockets(node, data);
              })
              .then()
              .catch((e) => {
                this.editor.emit({ type: 'clear' });
                this.sendErrorEvent('Network request failed.');
                return this.editor.removeNode(node.id);
              })
              .then(() => this.editor.emit({ type: 'cleared' }));
          }

          return node;
        },
      ]),
    ]);

    const contextMenu = new ContextMenuPlugin<Schemes>({
      items: ContextMenuPresets.classic.setup(menuItems),
    });

    this.area.use(contextMenu);
  }

  private groupByCategory(
    modules: Array<ModuleBlueprint>
  ): Map<string, Array<ModuleBlueprint>> {
    const map: Map<string, Array<ModuleBlueprint>> = new Map();
    modules.forEach((m) => {
      if (map.has(m.category)) {
        const modules = map.get(m.category);
        modules.push(m);
      } else {
        map.set(m.category, [m]);
      }
    });

    return map;
  }

  /**
   * Applies layouting algorithm to network.
   */
  async arrangeLayout() {
    await this.arrange.layout({
      options: {
        algorithm: 'layered',
        'elk.layered.spacing.nodeNodeBetweenLayers': '50',
      },
    });
  }

  /**
   * Export rete.js graph to serializable representation.
   *
   * @returns
   */
  export(): EditorNetwork {
    const nodeData: Array<ModuleOutput> = this.editor.getNodes().map((node) => {
      // view holds position information
      let nodeView = this.area.nodeViews.get(node.id);
      // moduleNode holds actual data about module
      let moduleNode = node as ModuleNode;

      // update position of module based on current view
      return {
        ...moduleNode.moduleInstance.module,
        position: {
          x: nodeView.position.x,
          y: nodeView.position.y,
        },
      };
    });

    const connectionData = this.editor.getConnections().map((c) => {
      return {
        id: c.id,
        sourceModule: c.source,
        sourceSocket: c.sourceOutput,
        targetModule: c.target,
        targetSocket: c.targetInput,
      };
    });

    return {
      modules: nodeData,
      connections: connectionData,
    };
  }

  async clear() {
    await this.editor.clear();
  }

  private sendErrorEvent(message: string) {
    this.eventSubject.next({
      type: EventType.ERROR,
      message: message,
    });
  }
}

export function createModuleInstance(
  moduleBlueprint: ModuleBlueprint
): ModuleInstance {
  return {
    module: {
      id: uuid(),
      label: moduleBlueprint.title,
      blueprint: moduleBlueprint.id,
      position: { x: 0, y: 0 },
      input_sockets: [],
      output_sockets: [],
    },
    blueprint: moduleBlueprint,
    icon: '',
  };
}
