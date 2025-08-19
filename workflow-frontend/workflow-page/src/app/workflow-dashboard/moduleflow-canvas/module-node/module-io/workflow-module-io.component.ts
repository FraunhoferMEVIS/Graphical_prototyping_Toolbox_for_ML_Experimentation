import { Component, Input } from '@angular/core';
import { ModuleOutput } from 'src/app/workflow-dashboard/models/module-output';
@Component({
  selector: 'workflow-module-io',
  templateUrl: './workflow-module-io.component.html',
  styleUrls: ['./workflow-module-io.component.css']
})
export class WorkflowModuleIOComponent {

  @Input() ioList!: Array<ModuleOutput>;

}
