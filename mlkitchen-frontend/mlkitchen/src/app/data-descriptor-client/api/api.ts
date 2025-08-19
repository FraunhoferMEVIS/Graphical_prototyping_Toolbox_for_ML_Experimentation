export * from './configuration.service';
import { ConfigurationService } from './configuration.service';
export * from './default.service';
import { DefaultService } from './default.service';
export * from './features.service';
import { FeaturesService } from './features.service';
export * from './modules.service';
import { ModulesService } from './modules.service';
export const APIS = [ConfigurationService, DefaultService, FeaturesService, ModulesService];
