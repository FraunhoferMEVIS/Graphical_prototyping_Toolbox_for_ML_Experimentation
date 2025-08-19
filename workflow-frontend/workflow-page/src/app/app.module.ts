import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { NgIconsModule } from '@ng-icons/core';
import { matOpenInNewRound } from '@ng-icons/material-icons/round';
import { WorkflowDashboardComponent } from './workflow-dashboard/workflow-dashboard.component';
import { AppComponent } from './app.component';
import { ModuleBar } from './workflow-dashboard/module-bar/module-bar.component';
import { ModuleCard } from './workflow-dashboard/module-bar/module-card/module-card.component';
import {
  Draggable,
  Droppable,
} from './helpers/drag-n-drop/drag-and-drop.directive';
import { Moveable } from './helpers/move/move.directive';
import { ModuleflowCanvasComponent } from './workflow-dashboard/moduleflow-canvas/moduleflow-canvas.component';
import { ModuleNodeComponent } from './workflow-dashboard/moduleflow-canvas/module-node/module-node.component';
import { ReteModule } from 'rete-angular-plugin/16';
import { ModuleStateComponent } from './workflow-dashboard/moduleflow-canvas/module-node/module-status/module-state.component';
import { WorkflowModuleIOComponent } from './workflow-dashboard/moduleflow-canvas/module-node/module-io/workflow-module-io.component';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { environment } from 'src/environments/environment';
import {
  ApiModule as Project_Manager_ApiModule,
  BASE_PATH as Project_Manager_BASE_PATH,
} from './api/project-manager';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NewProjectDialogComponent } from './topbar/new-project-dialog/new-project-dialog.component';
import { MatDialogModule } from '@angular/material/dialog';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { ReactiveFormsModule } from '@angular/forms';
import { MatMenuModule } from '@angular/material/menu';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatListModule } from '@angular/material/list';
import { MatTableModule } from '@angular/material/table';
import { MatSortModule } from '@angular/material/sort';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { TopbarComponent } from './topbar/topbar.component';
import { SelectProjectDialogComponent } from './topbar/select-project-dialog/select-project-dialog.component';
import { ProjectListComponent } from './topbar/project-list/project-list.component';
import { ManageProjectDialogComponent } from './topbar/manage-project-dialog/manage-project-dialog.component';
import { ActionDialogComponent } from './topbar/action-dialog/action-dialog.component';
import { EditProjectDialogComponent } from './topbar/edit-project-dialog/edit-project-dialog.component';
import { AppRoutingModule } from './app-routing.module';
import { InfoDialogComponent } from './topbar/info-dialog/info-dialog.component';
import { PageNotFoundComponent } from './page-not-found/page-not-found.component';
import { WorkflowHomeComponent } from './workflow-home/workflow-home.component';

@NgModule({
  declarations: [
    AppComponent,
    WorkflowModuleIOComponent,
    WorkflowDashboardComponent,
    ModuleBar,
    ModuleCard,
    ModuleStateComponent,
    ModuleflowCanvasComponent,
    ModuleNodeComponent,
    Draggable,
    Droppable,
    Moveable,
    NewProjectDialogComponent,
    SelectProjectDialogComponent,
    TopbarComponent,
    ProjectListComponent,
    ManageProjectDialogComponent,
    ActionDialogComponent,
    InfoDialogComponent,
    EditProjectDialogComponent,
    PageNotFoundComponent,
    WorkflowHomeComponent,
  ],
  imports: [
    AppRoutingModule,
    BrowserModule,
    ReteModule,
    HttpClientModule,
    Project_Manager_ApiModule,
    NgIconsModule.withIcons({ matOpenInNewRound }),
    FormsModule,
    BrowserAnimationsModule,
    MatDialogModule,
    MatFormFieldModule,
    MatSelectModule,
    MatInputModule,
    MatButtonModule,
    MatIconModule,
    MatMenuModule,
    MatToolbarModule,
    MatSnackBarModule,
    ReactiveFormsModule,
    MatToolbarModule,
    MatListModule,
    MatTableModule,
    MatTooltipModule,
    MatSortModule,
    MatPaginatorModule,
    MatProgressSpinnerModule,
    MatCheckboxModule,
  ],
  providers: [
    {
      provide: Project_Manager_BASE_PATH,
      useValue: environment.projectManagerBasePath,
    },
  ],
  bootstrap: [AppComponent],
})
export class AppModule { }
matOpenInNewRound;
