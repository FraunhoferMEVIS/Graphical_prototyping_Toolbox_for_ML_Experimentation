import { Component, Input } from '@angular/core';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-topbar',
  templateUrl: './topbar.component.html',
  styleUrls: ['./topbar.component.scss'],
})
export class TopbarComponent {
  @Input() toolTitle: string = '';
  @Input() projectId: string | null = '';

  goToWorkflowPage() {
    window.location.href =
      environment.workflowPageBasePath + `?projectId=${this.projectId}`;
  }
}
