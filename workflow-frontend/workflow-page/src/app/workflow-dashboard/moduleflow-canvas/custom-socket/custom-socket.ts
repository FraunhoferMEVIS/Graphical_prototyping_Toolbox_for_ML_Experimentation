import { ClassicPreset } from "rete";
import { ModuleInstance } from "../../models/module-instance";

export class CustomSocket extends ClassicPreset.Socket {

    moduleInstance: ModuleInstance = null;

    constructor(name: string, moduleInstance: ModuleInstance) {
        super(name);
        this.moduleInstance = moduleInstance;
    }

}