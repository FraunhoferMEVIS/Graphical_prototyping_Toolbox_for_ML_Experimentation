import { ClassicPreset } from 'rete';
import { ModuleNode } from './nodes';
import { ModuleInstance } from 'src/app/models/network';

export const NodeFactory = {
  // Defines whether a node can have multiple incoming connections at one socket.
  MULTIPLE_INPUTS: false,

  createModuleNode(moduleInstance: ModuleInstance) {
    const socket = new ClassicPreset.Socket('socket');
    const node = new ModuleNode(moduleInstance.blueprint.title, moduleInstance);

    // id of moduleInstance must be the same as the node id
    node.id = moduleInstance.module.id;

    moduleInstance.module.output_sockets.forEach((output) => {
      node.addOutput(
        output.name,
        new ClassicPreset.Output(socket, output.name)
      );
    });

    moduleInstance.module.input_sockets.forEach((input) => {
      node.addInput(
        input.name,
        new ClassicPreset.Input(socket, input.name, NodeFactory.MULTIPLE_INPUTS)
      );
    });

    return node;
  },
};
