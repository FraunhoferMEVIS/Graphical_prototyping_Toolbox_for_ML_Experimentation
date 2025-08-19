import { ModuleInstance } from "./models/network";

/**
 * Test data for unit tests.
 */
export const TestData = {

    createModuleInstance(): ModuleInstance {
        return {
            module: {
                id: '123',
                label: 'my-label',
                position: { x: 0, y: 100 },
                blueprint: "A",
                input_sockets: [],
                output_sockets: []
            },
            blueprint: {
                id: 'table',
                category: 'Table',
                title: 'Input Table',
                subtitle: '',
                description: '',
            },
            icon: "my-icon"
        };
    }
}
