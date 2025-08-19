import { ExecutionState } from "./execution-state";
import { ModuleConnection } from "./module-connection";
import { ModuleInstance } from "./module-instance";
import { v4 as uuid } from "uuid";

export class Workflow {
    readonly id: string = uuid();
    estimatedRuntime?: number;
    state: ExecutionState = ExecutionState.NOT_EXECUTED;
    moduleInstances: Array<ModuleInstance>;
    connections: Array<ModuleConnection>;

    constructor(
        moduleInstances: Array<ModuleInstance> = Array(),
        connections: Array<ModuleConnection> = Array()
    ) {
        this.moduleInstances = moduleInstances;
        this.connections = connections;
    }
}