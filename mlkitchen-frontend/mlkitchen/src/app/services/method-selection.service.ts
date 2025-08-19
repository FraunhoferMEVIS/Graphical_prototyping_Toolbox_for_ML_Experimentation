import { Injectable } from '@angular/core';
import {
  BodyPostConfigRecipeAllPost,
  MethodsService,
  Steps,
  TaskTypes,
} from '../backend-client';
import { ActivatedRoute } from '@angular/router';
import { Observable, first } from 'rxjs';
import {
  FormBuilder,
  Validators,
  FormGroup,
  FormControl,
} from '@angular/forms';
import { Method, Parameter } from '../models/method';
import { Filters } from '../backend-client';
import { FeaturesService } from '../data-descriptor-client';
import { RecipeService } from '../backend-client';
import { CookbookService } from './cookbook.service';
import { ConfigurationService } from '../data-descriptor-client';

export interface stepInformation {
  id: number;
  name: string;
  cookbookName: string;
  displayName: string;
  options$: Observable<any>;
  formGroup: FormGroup;
}

@Injectable({
  providedIn: 'root',
})
export class MethodSelectionService {
  public steps: stepInformation[] = [
    {
      id: 1,
      name: 'DataSplitting',
      cookbookName: 'split',
      displayName: 'Data Splitting',
      options$: new Observable<any>(),
      formGroup: new FormGroup({
        selectedOptions: new FormControl<Method[]>([]),
      }),
    },
    {
      id: 2,
      name: 'Encoders',
      cookbookName: 'encoders',
      displayName: 'Encoders',
      options$: new Observable<any>(),
      formGroup: new FormGroup({
        selectedOptions: new FormControl<Method[]>([]),
      }),
    },
    {
      id: 3,
      name: 'HandlingMissingValues',
      cookbookName: 'imputation',
      displayName: 'Missing Values',
      options$: new Observable<any>(),
      formGroup: new FormGroup({
        selectedOptions: new FormControl<Method[]>([]),
      }),
    },
    {
      id: 4,
      name: 'FeatureSelection',
      cookbookName: '',
      displayName: 'Feature Selection',
      options$: new Observable<any>(),
      formGroup: new FormGroup({
        selectedOptions: new FormControl<Method[]>([]),
      }),
    },
    {
      id: 5,
      name: 'Estimator',
      cookbookName: 'estimator',
      displayName: 'Estimators',
      options$: new Observable<any>(),
      formGroup: new FormGroup({
        selectedOptions: new FormControl<Method[]>([]),
      }),
    },
    {
      id: 6,
      name: 'Metric',
      cookbookName: 'metrics',
      displayName: 'Metrics',
      options$: new Observable<any>(),
      formGroup: new FormGroup({
        selectedOptions: new FormControl<Method[]>([]),
      }),
    },
  ];

  public descriptionFormGroup = this._formBuilder.group({
    name: ['', Validators.required],
    description: [''],
    creator: [''],
    target: [''],
    type: ['', Validators.required],
    language: ['python', Validators.required],
    positive_class: [''],
  });
  public summaryFormGroup = this._formBuilder.group({});
  public generalFormGroup = this._formBuilder.group({
    search: [''],
    mode: ['options'],
  });

  public projectName: string = '';
  public dataDescription$: Observable<any> = new Observable<any>();
  public hyperparameterTuning$: Observable<any> = new Observable<any>();
  public selectedStep: number = 0;
  public encodersNumerical: string[] = [];
  public encodersCategorical: string[] = [];

  constructor(
    private methodsService: MethodsService,
    private featuresService: FeaturesService,
    private recipeService: RecipeService,
    private _formBuilder: FormBuilder,
    private cookbookService: CookbookService,
    public route: ActivatedRoute,
    private configurationService: ConfigurationService
  ) {
    this.createOptionsOberservables([]);
    this.retrieveDataMetaInformation();
    this.methodsService
      .getImplementedMethodsMethodsStepGet('Encoders', 'numerical')
      .pipe(first())
      .subscribe((result) => {
        this.encodersNumerical = result.algorithms[0].algorithms;
      });
    this.methodsService
      .getImplementedMethodsMethodsStepGet('Encoders', 'categorical')
      .pipe(first())
      .subscribe((result) => {
        this.encodersCategorical = result.algorithms[0].algorithms;
      });
  }

  private createOptionsOberservables(filters: Filters[]): void {
    for (let s of this.steps) {
      s.options$ = this.setObservableForStep(s.name as Steps, filters);
    }
    this.hyperparameterTuning$ = this.setObservableForStep(
      'HyperparameterTuning',
      filters
    );
  }

  public setObservableForStep(step: Steps, filters: Filters): Observable<any> {
    return this.methodsService.getImplementedMethodsMethodsStepGet(
      step,
      filters
    );
  }

  public getSearchValueChange(): Observable<string | null> {
    return this.generalFormGroup.controls.search.valueChanges;
  }

  public getMethodWithName(name: string, step: Steps): Observable<any> {
    return this.methodsService.getMethodMetadataMethodsStepAlgGet(step, name);
  }

  public getSelectedOptions(step: Steps): Method[] {
    return this.steps.find((s) => s.name === step)?.formGroup.controls[
      'selectedOptions'
    ].value as Method[];
  }

  public setSelectedOptions(step: Steps, options: Method[]): void {
    this.steps
      .find((s) => s.name === step)
      ?.formGroup.controls['selectedOptions'].setValue(options);
  }

  public getNumberSelectedAlgorithms(): number {
    let selected = 0;
    for (let s of this.steps) {
      selected += (s.formGroup.controls['selectedOptions'].value! as Method[])
        .length;
    }
    return selected;
  }

  private retrieveDataMetaInformation(): void {
    this.route.queryParamMap.subscribe((params) => {
      this.projectName = params.get('projectId') as string;
      if (this.projectName) {
        this.dataDescription$ =
          this.featuresService.listOfProjectFeaturesFeaturesProjectIdListGet(
            this.projectName
          );
        this.configurationService
          .getCurrentMetadataConfigProjectIdGet(this.projectName)
          .pipe(first())
          .subscribe((config) => {
            if (!this.descriptionFormGroup.controls.target.value) {
              this.descriptionFormGroup.controls.target.setValue(config.target);
            }
          });
      }
    });
  }

  toNumber(value: string): number | string {
    const asNumber = Number(value);
    if (!isNaN(asNumber)) {
      return asNumber;
    } else {
      return value;
    }
  }

  public postConfigToBackend(): Observable<string> {
    const post = this.generateRecipePost();
    console.log(post);
    return this.recipeService.postConfigRecipeAllPost(post);
  }

  // just test recipe creation for now
  private generateRecipePost(): BodyPostConfigRecipeAllPost {
    const post: BodyPostConfigRecipeAllPost = {
      project: {
        name: this.descriptionFormGroup.controls.name.value as string,
      },
      config: {
        username: this.descriptionFormGroup.controls.creator.value as string,
        description: this.descriptionFormGroup.controls.description
          .value as string,
        task: this.descriptionFormGroup.controls.type.value as TaskTypes,
        target_col: this.descriptionFormGroup.controls.target.value as string,
        positive_class: this.toNumber(
          this.descriptionFormGroup.controls.positive_class.value as string
        ),
        split: this.cookbookService.methodListToConfig(
          this.getSelectedOptions('DataSplitting'),
          'DataSplitting'
        )[0],
        imputation: this.cookbookService.methodListToConfig(
          this.getSelectedOptions('HandlingMissingValues'),
          'HandlingMissingValues'
        ),
        encoders: this.cookbookService.methodListToConfig(
          this.getSelectedOptions('Encoders'),
          'Encoders'
        ),
        metrics: this.cookbookService.methodListToConfig(
          this.getSelectedOptions('Metric'),
          'Metric'
        ),
        //add checkbox later
        //choose first for now
        primaryMetric: this.cookbookService.methodListToConfig(
          this.getSelectedOptions('Metric'),
          'Metric'
        )[0].name,
        estimator: this.cookbookService.methodListToConfig(
          this.getSelectedOptions('Estimator'),
          'Estimator'
        ),
      },
    };
    console.log(post);
    return post as BodyPostConfigRecipeAllPost;
  }

  public loadExistingProject(project: string): void {
    this.recipeService
      .getConfigRecipeGetConfigGet(project)
      .pipe(first())
      .subscribe((res) => {
        console.log(res);
        if (res.task) {
          this.loadCookbook(res);
        }
      });
  }

  private loadCookbook(cookbook: any): void {
    this.descriptionFormGroup.controls.creator.setValue(cookbook.username);
    this.descriptionFormGroup.controls.description.setValue(
      cookbook.description
    );
    this.descriptionFormGroup.controls.type.setValue(cookbook.task);
    this.descriptionFormGroup.controls.target.setValue(cookbook.target_col);
    this.descriptionFormGroup.controls.positive_class.setValue(
      cookbook.positive_class
    );
    for (let s of this.steps) {
      if (s.cookbookName) {
        if (s.name !== 'DataSplitting') {
          this.setSelectedOptions(
            s.name as Steps,
            this.cookbookService.cookbookToMethodList(
              cookbook[s.cookbookName],
              s.name as Steps
            )
          );
        }
      }
    }
    let splitting: Method[];
    if (!Array.isArray(cookbook.split) && !cookbook.split.name) {
      splitting = [
        {
          step: 'DataSplitting',
          name: '',
          ratio: cookbook.split.ratio,
          parameters: this.cookbookParametersToMethodParameters(
            cookbook.split.parameters
          ),
        },
      ];
    } else {
      splitting = this.cookbookService.cookbookToMethodList(
        cookbook.split,
        'DataSplitting'
      );
    }
    this.setSelectedOptions('DataSplitting', splitting);
  }

  private cookbookParametersToMethodParameters(
    cookbookParameters: Object
  ): Parameter[] {
    if (!cookbookParameters) {
      return [];
    }
    let parameters: Parameter[] = [];
    for (let [key, value] of Object.entries(cookbookParameters)) {
      let parameter: Parameter = {
        name: key,
        value: value,
      };
      parameters.push(parameter);
    }
    return parameters;
  }
}
