import { ModuleType } from "./module-type"

export interface ModuleOutput {
    id: string
    timestamp: String
    moduleId: String
    payload?: String
    meta?: {
        label: String
    }
    // maybe Ids of allowed module inputs
    allowedInputs?: Array<ModuleType>
}