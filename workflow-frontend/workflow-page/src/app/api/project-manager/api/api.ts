export * from './default.service';
import { DefaultService } from './default.service';
export * from './projects.service';
import { ProjectsService } from './projects.service';
export const APIS = [DefaultService, ProjectsService];
