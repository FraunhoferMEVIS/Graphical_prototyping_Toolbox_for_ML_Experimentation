import { Environment } from './environment-type';

export const windowEnv = (window as any)['env'];
export const environment: Environment = {
  backendBasePath: windowEnv?.['backendBasePath'] || '',
  projectManagerBasePath: windowEnv?.['projectManagerBasePath'] || '',
  dataDescriptorBasePath: windowEnv?.['dataDescriptorBasePath'] || '',
  workflowPageBasePath: windowEnv?.['workflowPageBasePath'] || '',
};
