import { ClassicPreset } from "rete";
import { ModuleInstance } from "../models/module-instance";

export class Node extends ClassicPreset.Node {
    // width and height is required for autoarrange plugin
    // TODO: duplicated in vars.sass, find a way to define this once
    // for use in css and in code
    width = 300;
    height = 280;
}

export class ModuleNode extends Node {

    moduleInstance: ModuleInstance

    constructor(label: string, moduleInstance: ModuleInstance) {
        super(label);
        this.moduleInstance = moduleInstance;
    }
}
