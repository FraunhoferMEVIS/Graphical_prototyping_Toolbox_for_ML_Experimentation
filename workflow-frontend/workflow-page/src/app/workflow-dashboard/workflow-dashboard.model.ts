import { Module } from "./models/module";
import { ModuleInstance } from "./models/module-instance";

export interface ModuleList extends Array<Module> { }

export type ModuleInstances = Array<ModuleInstance>;

export interface ModuleIOFlowList extends Array<ModuleIOFlow> { }

export interface ModuleIOFlow {
    from: String, // Module ID
    to: String // Module ID
}

