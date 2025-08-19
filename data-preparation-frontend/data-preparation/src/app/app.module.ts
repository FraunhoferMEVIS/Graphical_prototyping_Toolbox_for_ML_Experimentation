import { BrowserModule } from '@angular/platform-browser';
import { ErrorHandler, NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatButtonModule } from '@angular/material/button';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatIconModule } from '@angular/material/icon';
import { MatListModule } from '@angular/material/list';
import { CanvasComponent } from './components/canvas/canvas.component';
import { CustomNodeComponent } from './components/canvas/custom-node/custom-node.component';
import { CustomConnectionComponent } from './components/canvas/custom-connection/custom-connection.component';
import { CustomSocketComponent } from './components/canvas/custom-socket/custom-socket.component';
import { ButtonComponent } from './components/canvas/controls/custom-button.component';
import { ReteModule } from 'rete-angular-plugin/16';
import { MatDialogModule } from '@angular/material/dialog';
import { ModuleConfigDialogComponent } from './components/dialogs/module-config-dialog/module-config-dialog.component';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatSelectModule } from '@angular/material/select';
import { MatMenuModule } from '@angular/material/menu';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import {
  Draggable,
  Droppable,
} from './helpers/drag-n-drop/drag-and-drop.directive';
import { Moveable } from './helpers/move/move.directive';
import { CdkDrag } from '@angular/cdk/drag-drop';
import { PreviewDialogComponent } from './components/dialogs/preview-dialog/preview-dialog.component';
import { TableComponent } from './components/dialogs/preview-dialog/table/table.component';
import { MatTableModule } from '@angular/material/table';
import { ChartComponent } from './components/dialogs/preview-dialog/chart/chart.component';
import { ReactiveFormsModule } from '@angular/forms';
import { FormsModule } from '@angular/forms';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { HttpClientModule } from '@angular/common/http';
import { DemoPlotComponent } from './components/dialogs/preview-dialog/demo-plot/demo-plot.component';
import { MatPaginatorModule } from '@angular/material/paginator';
import { ModulesListComponent } from './components/dashboard/modules-list/modules-list.component';
import { ImagePlotComponent } from './components/dialogs/preview-dialog/image-plot/image-plot.component';
import { ActionDialogComponent } from './components/dialogs/action-dialog/action-dialog.component';
import { GlobalErrorHandler } from './helpers/error-handler';
import { ErrorDialogComponent } from './components/dialogs/error-dialog/error-dialog.component';
import { MatChipsModule } from '@angular/material/chips';
import { ChipListControlComponent } from './components/dialogs/module-config-dialog/chip-control/chip-list-control.component';
import { ModulesListNestedComponent } from './components/dashboard/modules-list-nested/modules-list-nested.component';
import { HelpDialog } from './components/dialogs/help-dialog/help-dialog.component';

@NgModule({
  declarations: [
    AppComponent,
    DashboardComponent,
    CanvasComponent,
    CustomNodeComponent,
    CustomConnectionComponent,
    CustomSocketComponent,
    ButtonComponent,
    ModuleConfigDialogComponent,
    Draggable,
    Droppable,
    Moveable,
    PreviewDialogComponent,
    TableComponent,
    ChartComponent,
    DemoPlotComponent,
    ModulesListComponent,
    ImagePlotComponent,
    ActionDialogComponent,
    ErrorDialogComponent,
    ChipListControlComponent,
    ModulesListNestedComponent,
    HelpDialog,
  ],
  imports: [
    // Rete
    ReteModule,
    // Material UI
    MatDialogModule,
    MatToolbarModule,
    MatSidenavModule,
    MatIconModule,
    MatListModule,
    MatFormFieldModule,
    MatButtonModule,
    MatInputModule,
    MatSelectModule,
    MatMenuModule,
    MatTooltipModule,
    MatCheckboxModule,
    MatSnackBarModule,
    MatPaginatorModule,
    MatTableModule,
    MatChipsModule,
    MatProgressSpinnerModule,
    // Angular
    ReactiveFormsModule,
    FormsModule,
    CdkDrag,
    BrowserModule,
    BrowserAnimationsModule,
    // API
    HttpClientModule,
  ],
  providers: [{ provide: ErrorHandler, useClass: GlobalErrorHandler }],
  bootstrap: [AppComponent],
})
export class AppModule {}
