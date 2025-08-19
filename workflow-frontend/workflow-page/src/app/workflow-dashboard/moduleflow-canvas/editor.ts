import { Injector } from '@angular/core';
import { NodeEditor, GetSchemes, ClassicPreset } from 'rete';
import { AreaPlugin, AreaExtensions } from 'rete-area-plugin';
import {
  ConnectionPlugin,
  Presets as ConnectionPresets,
} from 'rete-connection-plugin';
import { AngularPlugin, Presets, AngularArea2D } from 'rete-angular-plugin/15';
import { Workflow } from '../models/workflow';
import {
  ButtonComponent,
  ButtonControl,
} from './controls/custom-button.component';
import { ModuleNode, Node } from './module-node';
import {
  AutoArrangePlugin,
  Presets as ArrangePresets,
} from 'rete-auto-arrange-plugin';
import { ModuleNodeComponent } from './module-node/module-node.component';
import { ModuleInstance } from '../models/module-instance';
import { CustomConnectionComponent } from './custom-connection/custom-connection.component';
import { CustomSocketComponent } from './custom-socket/custom-socket.component';
import {
  ContextMenuExtra,
  ContextMenuPlugin,
  Presets as ContextMenuPresets,
} from 'rete-context-menu-plugin';
import { MODULES } from '../workflow-dashboard.config';
import { ItemDefinition } from 'rete-context-menu-plugin/_types/presets/classic/types';
import { CustomSocket } from './custom-socket/custom-socket';
import { ModuleType } from '../models/module-type';
import { ReadonlyPlugin } from 'rete-readonly-plugin';

export class Connection<N extends Node> extends ClassicPreset.Connection<
  N,
  N
> {}
export type Schemes = GetSchemes<Node, Connection<Node>>;
type AreaExtra = AngularArea2D<Schemes> | ContextMenuExtra;

type NodeMap = {
  [key: string]: Node;
};

// identifier of input and output socket.
// for now we use the same identifier since we only have 1 input and 1 output socket.
const PORT_ID: string = 'port';

// Defines whether a node can have multiple incoming connections at one socket.
const MULTIPLE_INPUTS: boolean = true;

/**
 * A wrapper of three.js, offering a high-level interface to manage the workflow visualization.
 */
export class Editor {
  // Editor specific instances
  private editor: NodeEditor<Schemes>;
  private area: AreaPlugin<Schemes, AreaExtra>;
  private arrange: AutoArrangePlugin<Schemes>;
  private readonly: ReadonlyPlugin<Schemes>;

  constructor(
    container: HTMLElement,
    injector: Injector,
    public project: string = ''
  ) {
    const editor = new NodeEditor<Schemes>();
    const area = new AreaPlugin<Schemes, AreaExtra>(container);
    const connection = new ConnectionPlugin<Schemes, AreaExtra>();
    const render = new AngularPlugin<Schemes, AreaExtra>({ injector });
    const arrange = new AutoArrangePlugin<Schemes>();
    const readonly = new ReadonlyPlugin<Schemes>();

    this.readonly = readonly;
    this.arrange = arrange;
    this.area = area;
    this.editor = editor;

    const menuItems: ItemDefinition<Schemes>[] = MODULES.map((m) => [
      m.subtitle,
      () => this.createModuleNode(ModuleInstance.fromModule(m)),
    ]);

    // const contextMenu = new ContextMenuPlugin<Schemes>({
    //   items: ContextMenuPresets.classic.setup(menuItems),
    // });
    // area.use(contextMenu);
    arrange.addPreset(ArrangePresets.classic.setup());
    area.use(arrange);

    AreaExtensions.selectableNodes(area, AreaExtensions.selector(), {
      accumulating: AreaExtensions.accumulateOnCtrl(),
    });

    render.addPreset(Presets.contextMenu.setup());
    render.addPreset(
      Presets.classic.setup({
        customize: {
          node() {
            return ModuleNodeComponent;
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
      })
    );

    connection.addPreset(ConnectionPresets.classic.setup());

    editor.use(readonly.root);
    editor.use(area);

    area.use(readonly.area);
    area.use(render);

    area.use(connection);

    this.area.addPipe((context) => {
      // prevent dragging, zooming and moving
      if (!readonly.enabled) return context;
      if (context.type === 'nodetranslate') return null;
      if (context.type === 'translate') return null;
      if (context.type === 'zoom') return null;
      return context;
    });

    connection.addPipe((context) => {
      if (!readonly.enabled) {
        return context;
      }
      if (context.type === 'connectionpick') {
        return null;
      }

      return context;
    });

    // Resize area when window resizes
    addEventListener('resize', (event) => {
      this.readonly.disable();
      AreaExtensions.zoomAt(this.area, this.editor.getNodes()).then(() => {
        this.readonly.enable();
      });
    });

    AreaExtensions.simpleNodesOrder(area);
  }

  private enableReadOnly() {
    this.readonly.enable();
  }

  private disableReadOnly() {
    this.readonly.disable();
  }

  async addModule(
    elementX: number = 0,
    elementY: number = 0,
    module: ModuleInstance
  ) {
    const node = this.createModuleNode(module);

    // TODO: fix the use of the zoom level 'k', not working properly once zoom level changes
    // actual coordinates of the area
    // https://retejs.org/docs/faq#viewport-center
    const { x, y, k } = this.area.area.transform;

    // calculate offset so that div is added in the center of the passed (x, y) point.
    let offsetX = node.width / 2 / k;
    let offsetY = node.height / 2 / k;

    // calculate insertion point in area
    const transformedX = elementX + x - offsetX;
    const transformedY = elementY - y - offsetY;

    // const centerPosition = this.getViewPortCenter();
    var firstNode = this.editor.getNodes().length == 0;
    await this.editor.addNode(node);
    await this.area.translate(node.id, { x: transformedX, y: transformedY });
    await this.area.translate(node.id, this.area.area.pointer);

    if (firstNode) {
      // center canvas on first node
      AreaExtensions.zoomAt(this.area, this.editor.getNodes());
    }

    return () => this.area.destroy();
  }

  /**
   * Triggers an update of all node components in the canvas.
   *
   * Node components will re-render on update.
   */
  async updateNodes() {
    this.disableReadOnly();

    for (let n of this.editor.getNodes()) {
      await this.area.update('node', n.id);
    }

    this.enableReadOnly();
  }

  /**
   * Create a rete.js graph based on {@param workflow}.
   *
   * @param workflow
   */
  async importWorkflow(workflow: Workflow) {
    this.disableReadOnly();

    // make sure we start on empty canvas.
    await this.editor.clear();

    if (workflow == null) {
      return Promise.resolve();
    }

    var shift = 0;
    var nodeMap: NodeMap = {};

    // (1) create the nodes and store them in a map
    for (let moduleInstances of workflow.moduleInstances) {
      const node: Node = this.createModuleNode(moduleInstances);
      nodeMap[moduleInstances.id] = node;

      await this.editor.addNode(node);

      var y = 0;
      if (moduleInstances.module.type == ModuleType.ML_GUIDE) {
        y = 150;
      } else if (moduleInstances.module.type == ModuleType.ML_KITCHEN) {
        y = -150;
      }
      await this.area.translate(node.id, { x: shift, y: y });
      shift += 350;
    }

    // (2) create connections by accessing node map
    for (let connection of workflow.connections) {
      let outputNode = nodeMap[connection.from];
      let inputNode = nodeMap[connection.to];

      await this.editor.addConnection(
        new Connection(outputNode, PORT_ID, inputNode, PORT_ID)
      );
    }

    // focus area on graph
    await AreaExtensions.zoomAt(this.area, this.editor.getNodes());

    this.enableReadOnly();

    return () => this.area.destroy();
  }

  async clear() {
    await this.editor.clear();
  }

  private createModuleNode(moduleInstance: ModuleInstance): ModuleNode {
    const node = new ModuleNode('module', moduleInstance);

    node.addControl(
      'button',
      new ButtonControl('Open', () => {
        window.location.href =
          moduleInstance.module.link + `?projectId=${this.project}`;
      })
    );

    const inputSocket = new CustomSocket('input', moduleInstance);
    const outputSocket = new CustomSocket('output', moduleInstance);

    node.addOutput(PORT_ID, new ClassicPreset.Output(outputSocket));
    node.addInput(
      PORT_ID,
      new ClassicPreset.Input(inputSocket, null, MULTIPLE_INPUTS)
    );

    return node;
  }
}
