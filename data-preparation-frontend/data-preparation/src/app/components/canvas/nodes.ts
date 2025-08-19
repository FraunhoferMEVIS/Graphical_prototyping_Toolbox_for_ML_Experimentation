import { ClassicPreset } from "rete";
import { ModuleInstance } from "src/app/models/network";

export const NODE_WIDTH = 200;
export const NODE_HEIGHT = 300;

export class Node extends ClassicPreset.Node {
    // width and height is required for autoarrange plugin
    // TODO: duplicated in vars.sass, find a way to define this once
    // for use in css and in code 
    public width = NODE_WIDTH;
    public height = NODE_HEIGHT;
}

export class ModuleNode extends Node {

    // identifier of input and output socket.
    // for now we use the same identifier since we only have 1 input and 1 output socket.
    static PORT_ID: string = 'port';

    moduleInstance: ModuleInstance

    constructor(label: string, moduleInstance: ModuleInstance) {
        super(label);
        this.moduleInstance = moduleInstance;
    }
}