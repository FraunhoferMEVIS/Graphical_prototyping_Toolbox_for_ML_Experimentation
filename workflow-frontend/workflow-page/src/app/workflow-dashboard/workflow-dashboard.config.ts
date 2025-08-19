import { ExecutionState } from './models/execution-state';
import { ModuleInstance } from './models/module-instance';
import { ModuleType } from './models/module-type';
import { Workflow } from './models/workflow';
import { WorkflowTemplate } from './models/workflow-template';
import { v4 as uuid } from 'uuid';
import { environment } from 'src/environments/environment';

/**
 * The modules that are available for use in the canvas.
 */
export const MODULES = [
  {
    id: 'maratus',
    type: ModuleType.MARATUS,
    title: 'Cohort Selection & Data Preparation',
    subtitle: 'maratus',
    icon: 'assets/logos/maratusLogo.png',
    description:
      'This FDZ data exploration and visualization tool enables you to get a first impression of possible correlations, sample sizes and data quality.\n\nOnce a satisfying data selection has been found, it is possible to export that selection and make it available to other tools inside the AI-Sandbox.',
    link: environment.maratusBasePathFrontend,
  },
  {
    id: 'mlkitchen',
    type: ModuleType.ML_KITCHEN,
    title: 'Experiment Builder',
    subtitle: 'mlkitchen',
    icon: 'assets/logos/mlkitchenLogo.png',
    description:
      'mlkitchen enables you to create and execute so called "mlflow recipes" from a selection of available algorithms. These recipes define a series of steps to perform during a machine learning experiment. Created code, models and artefacts are send to the mlflow tracking server so that the results of different iterations of an experiment can be compared.',
    link: environment.mlkitchenBasePathFrontEnd,
  },
  {
    id: 'mlflow',
    type: ModuleType.ML_FLOW_TRACKING,
    title: 'Experiment Results',
    subtitle: 'mlflow tracking server',
    icon: 'assets/logos/mlflowLogo.png',
    description:
      'This open source software provides version control for machine learning experiments. It enables you to compare source code and performance between different versions of an experiment and stores the generated models in a registry.',
    link: environment.mlflowBasePath,
  }
];

const maratusInstance = new ModuleInstance(
  uuid(),
  ExecutionState.NOT_EXECUTED,
  MODULES[0],
  {
    in: [],
    out: [],
  }
);

const mlKitchenInstance = new ModuleInstance(
  uuid(),
  ExecutionState.NOT_EXECUTED,
  MODULES[1],
  {
    in: [],
    out: [],
  }
);

const mlFlowInstance = new ModuleInstance(
  uuid(),
  ExecutionState.NOT_EXECUTED,
  MODULES[2],
  {
    in: [],
    out: [],
  }
);

export const BASIC_WORKFLOW_TEMPLATE: WorkflowTemplate = {
  id: uuid(),
  name: 'Basic Template',
  workflow: new Workflow(
    [maratusInstance, mlKitchenInstance, mlFlowInstance],
    [
      { from: maratusInstance.id, to: mlKitchenInstance.id },
      { from: mlKitchenInstance.id, to: mlFlowInstance.id },
    ]
  ),
};
