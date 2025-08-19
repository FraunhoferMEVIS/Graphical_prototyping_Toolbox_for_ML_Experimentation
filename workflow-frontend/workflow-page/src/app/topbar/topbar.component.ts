import { Component, EventEmitter, Output } from '@angular/core';
import { Theme } from '../workflow-home/workflow-home.component';
import { MatDialog } from '@angular/material/dialog';
import { DashboardService } from '../workflow-dashboard/workflow-dashboard.service';
import { SelectProjectDialogComponent } from './select-project-dialog/select-project-dialog.component';
import { ManageProjectDialogComponent } from './manage-project-dialog/manage-project-dialog.component';
import {
  BASIC_WORKFLOW_TEMPLATE
} from '../workflow-dashboard/workflow-dashboard.config';
import { InfoDialogComponent } from './info-dialog/info-dialog.component';
import { environment } from 'src/environments/environment';

// TODO: remove this once we decide whether we need the info dialog.
const TASK_DESCRIPTION = `
 <p>
    This tool is designed to help you visualize and manage your processes more efficiently. Below is an overview of the key features and how to use them:
  </p>

  <h2>1. Tool Overview:</h2>
  <ul>
    <li><strong>Tool Palette:</strong> The left-hand panel displays all the available tools and functions you can use in your workflow. Each tool is categorized by type and functionality for easy access.</li>
    <li><strong>Search Functionality:</strong> Use the search bar above the tool palette to quickly find specific tools by name or keyword.</li>
    <li><strong>Tool Information:</strong> Hover over any tool to see a brief description of its function. Click on the tool to view more detailed information and configuration options.</li>
  </ul>

  <br>
  <h2>2. Workflow Canvas:</h2>
  <ul>
    <li><strong>Drag and Drop:</strong> Build your workflow by dragging tools from the palette onto the canvas. Arrange them to represent the sequence of operations.</li>
    <li><strong>Connect Tools:</strong> Click on the output of one tool and drag a line to the input of another to establish a data flow. Arrows will automatically appear to indicate the direction of the data flow.</li>
    <li><strong>Branching and Merging:</strong> You can create branches by connecting one tool's output to multiple tools' inputs. Likewise, you can merge data from different tools into a single tool.</li>
  </ul>

  <br>
  <h2>3. Data Flow Visualization:</h2>
  <ul>
    <li><strong>Real-Time Updates:</strong> The canvas dynamically updates to reflect any changes in your workflow, showing how data moves through each step.</li>
    <li><strong>Color Coding:</strong> Different types of data flows are color-coded for easier identification. For example, input data may be blue, while output data is green.</li>
    <li><strong>Error Indicators:</strong> If there’s a break or error in your workflow, the affected tool or connection will be highlighted in red, with a tooltip explaining the issue.</li>
  </ul>
`;

@Component({
  selector: 'app-topbar',
  templateUrl: './topbar.component.html',
  styleUrls: ['./topbar.component.css'],
})
export class TopbarComponent {
  @Output() themeEvent = new EventEmitter<Theme>();

  constructor(
    public dashboardService: DashboardService,
    public dialog: MatDialog
  ) { }

  onThemeSelected(theme: Theme) {
    this.themeEvent.emit(theme);
  }

  onManageProjects() {
    this.dialog.open(ManageProjectDialogComponent, {
      data: { title: 'Manage Projects' },
      minWidth: '90%',
    });
  }

  onOpenProject() {
    this.dialog.open(SelectProjectDialogComponent, {
      data: {
        title: 'Open project',
      },
      minWidth: '30%',
    });
  }

  onTemplateBasicClick() {
    this.dashboardService.loadWorkflow(BASIC_WORKFLOW_TEMPLATE);
  }

  onInfoClick() {
    this.dialog.open(InfoDialogComponent, {
      data: {
        title: 'Tool Info',
        description: TASK_DESCRIPTION,
      },
    });
  }
}
