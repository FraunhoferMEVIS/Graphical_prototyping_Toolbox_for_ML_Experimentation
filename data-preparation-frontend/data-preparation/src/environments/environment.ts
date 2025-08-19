import { Environment } from './environment-type';

export const windowEnv = (window as any)['env'];
export const environment: Environment = {
  production: true,
  projectManagerBasePath: windowEnv?.['projectManagerBasePath'] || '',
  dataPreparationBasePath: windowEnv?.['dataPreparationBasePath'] || '',
  workflowPageBasePath: windowEnv?.['workflowPageBasePath'] || '',
};
