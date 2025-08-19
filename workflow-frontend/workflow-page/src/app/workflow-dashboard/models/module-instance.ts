import { ExecutionState } from "./execution-state"
import { Module } from "./module"
import { ModuleOutput } from "./module-output"
import { v4 as uuid } from "uuid";

type Data = {
    in: Array<ModuleOutput>,
    out: Array<ModuleOutput>
}

export class ModuleInstance {

    constructor(
        public readonly id: string,
        public state: ExecutionState,
        public readonly module: Module,
        public data: Data
    ) {
    };

    static fromModule(module: Module): ModuleInstance {
        return new ModuleInstance(
            uuid(),
            ExecutionState.NOT_EXECUTED,
            module,
            { in: [], out: [] }
        );
    }
}