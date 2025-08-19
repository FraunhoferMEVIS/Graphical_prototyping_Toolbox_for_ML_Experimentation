import { Environment } from './environment-type';

export const windowEnv = (window as any)['env'];
export const environment: Environment = {
  production: true,
  maratusBasePathFrontend: windowEnv?.['maratusBasePathFrontend'] || '',
  mlkitchenBasePathFrontEnd: windowEnv?.['mlkitchenBasePathFrontEnd'] || '',
  mlflowBasePath: windowEnv?.['mlflowBasePath'] || '',
  projectManagerBasePath: windowEnv?.['projectManagerBasePath'] || '',
};
