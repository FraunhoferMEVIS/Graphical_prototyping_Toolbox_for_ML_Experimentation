import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatButtonModule } from '@angular/material/button';
import { NgIf } from '@angular/common';
import { MatSidenavModule } from '@angular/material/sidenav';
import { SidenavComponent } from './sidenav/sidenav.component';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';
import { MatStepperModule } from '@angular/material/stepper';
import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatSnackBarModule } from '@angular/material/snack-bar';
import { StepperComponent } from './stepper/stepper.component';
import { MatButtonToggleModule } from '@angular/material/button-toggle';
import { MethodSelectionService } from './services/method-selection.service';
import { DescriptionComponent } from './forms/description/description.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatGridListModule } from '@angular/material/grid-list';
import { MatDividerModule } from '@angular/material/divider';
import { MatBadgeModule } from '@angular/material/badge';
import { MatTableModule } from '@angular/material/table';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatCheckbox, MatCheckboxModule } from '@angular/material/checkbox';

import { AlgorithmSelectionComponent } from './forms/algorithms/algorithms.component';
import { MatToolbarModule } from '@angular/material/toolbar';
import {
  ApiModule as Backend_ApiModule,
  Configuration,
  ConfigurationParameters,
} from './backend-client';
import {
  ApiModule as Data_Descriptor_ApiModule,
  BASE_PATH as Data_Descriptor_BASE_PATH,
} from './data-descriptor-client';
import { environment } from 'src/environments/environment';
import { FlexLayoutModule } from '@angular/flex-layout';
import { SelectedOptionsComponent } from './templates/selected-options/selected-options.component';
import { AddAlgorithmDialogComponent } from './forms/algorithms/add-algorithm-dialog/add-algorithm-dialog.component';
import { MatDialogModule } from '@angular/material/dialog';
import { MatSelectModule } from '@angular/material/select';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatExpansionModule } from '@angular/material/expansion';
import { MatMenuModule } from '@angular/material/menu';
import { TopbarComponent } from './topbar/topbar.component';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';

export function apiConfigFactory(): Configuration {
  const params: ConfigurationParameters = {
    withCredentials: true,
    basePath: environment.backendBasePath,
  };
  return new Configuration(params);
}

@NgModule({
  declarations: [
    AppComponent,
    SidenavComponent,
    StepperComponent,
    DescriptionComponent,
    AlgorithmSelectionComponent,
    SelectedOptionsComponent,
    AddAlgorithmDialogComponent,
    TopbarComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MatButtonModule,
    NgIf,
    MatSidenavModule,
    MatSelectModule,
    MatIconModule,
    MatCardModule,
    MatStepperModule,
    MatBadgeModule,
    MatInputModule,
    MatFormFieldModule,
    MatSnackBarModule,
    MatButtonToggleModule,
    MatProgressSpinnerModule,
    MatSlideToggleModule,
    MatExpansionModule,
    MatDialogModule,
    MatTableModule,
    MatTooltipModule,
    HttpClientModule,
    MatMenuModule,
    FormsModule,
    ReactiveFormsModule,
    MatGridListModule,
    MatDividerModule,
    MatToolbarModule,
    MatCheckboxModule,
    FlexLayoutModule,
    Backend_ApiModule,
    Data_Descriptor_ApiModule,
  ],
  providers: [
    MethodSelectionService,
    {
      provide: Configuration,
      useValue: apiConfigFactory(),
    },
    {
      provide: Data_Descriptor_BASE_PATH,
      useValue: environment.dataDescriptorBasePath,
    },
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
