import { Injectable } from '@angular/core';
import createClient from 'openapi-fetch';
import { paths } from './schema';
import { environment } from 'src/environments/environment';
import { from } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ProjectManagerApi {
  private client = createClient<paths>({
    baseUrl: environment.dataPreparationBasePath,
  });

  export(projectId: string, toolId: string, targetId: string, payload: any) {
    return from(
      this.client.POST('/export/{project_id}/{source_tool}/{target_tool}', {
        params: {
          path: {
            project_id: projectId,
            source_tool: toolId,
            target_tool: targetId,
          },
        },
        body: payload,
      })
    );
  }
}
