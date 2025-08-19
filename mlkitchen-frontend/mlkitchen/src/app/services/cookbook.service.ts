import { Injectable } from '@angular/core';
import { Method, Parameter } from '../models/method';
import {
  MetricsConfig,
  ColumnTransformerConfig,
  AlgorithmConfig,
  NewFeatureConfig,
  SplitConfig,
  Steps,
} from '../backend-client';

@Injectable({
  providedIn: 'root',
})
export class CookbookService {
  constructor() {}

  public methodListToConfig(
    methodList: Method[],
    step: Steps
  ):
    | SplitConfig[]
    | ColumnTransformerConfig[]
    | MetricsConfig[]
    | AlgorithmConfig[]
    | NewFeatureConfig[] {
    switch (step) {
      case 'DataSplitting':
        return methodList.map((method) => ({
          name: method.name,
          language: method.language,
          parameters: this.methodParameterToConfig(method),
          ratio: method.ratio,
        })) as SplitConfig[];
      case 'HandlingMissingValues':
        return methodList.map((method) => ({
          name: method.name,
          language: method.language,
          parameters: this.methodParameterToConfig(method),
          column_name: method.column_name,
          all_numerical: method.all_numerical,
          all_categorical: method.all_categorical,
        })) as ColumnTransformerConfig[];
      case 'Encoders':
        return methodList.map((method) => ({
          name: method.name,
          language: method.language,
          parameters: this.methodParameterToConfig(method),
          column_name: method.column_name,
          all_numerical: method.all_numerical,
          all_categorical: method.all_categorical,
        })) as ColumnTransformerConfig[];
      case 'Metric':
        return methodList.map((method) => ({
          name: method.name,
          language: method.language,
          parameters: this.methodParameterToConfig(method),
          threshold: method.threshold,
          greater_is_better: method.greater_is_better,
        })) as MetricsConfig[];
      case 'Estimator':
        return methodList.map((method) => ({
          name: method.name,
          language: method.language,
          parameters: this.methodParameterToConfig(method),
        })) as AlgorithmConfig[];
      case 'FeatureSelection':
        return methodList.map((method) => ({
          name: method.name,
          language: method.language,
          parameters: this.methodParameterToConfig(method),
          column_name: method.column_name,
        })) as NewFeatureConfig[];
      default:
        return [];
    }
  }

  private methodParameterToConfig(method: Method): any {
    let config = {};
    method.parameters.forEach((parameter) => {
      config[parameter.name] = parameter.value;
    });
    if (method.hyperParameterTuning?.parameters.length) {
      config['n_iter'] = method.hyperParameterTuning.iterations;
      config['hyper_parameter_tuning'] =
        method.hyperParameterTuning.selectedTuningMethod;
      config['search_space'] = {};
      method.hyperParameterTuning.parameters.forEach((parameter) => {
        config['search_space'][parameter.name] = parameter.value;
      });
    }
    return config;
  }

  public cookbookToMethodList(configs: any[] | any, step): Method[] {
    let methods: Method[] = [];
    if (!configs) {
      return methods;
    }
    if (Array.isArray(configs)) {
      configs.forEach((config) => {
        methods.push(this.buildMethod(config, step));
      });
    } else {
      methods.push(this.buildMethod(configs, step));
    }
    return methods;
  }

  private buildMethod(config: any[] | any, step): any {
    let m: Method = {
      name: config.name,
      parameters: [],
      step: step,
      help: 'test',
    };

    if (config.parameters) {
      for (let [key, value] of Object.entries(config.parameters)) {
        if (
          key === 'n_iter' ||
          key === 'hyper_parameter_tuning' ||
          key === 'search_space'
        ) {
          continue;
        }
        m.parameters.push({
          name: key,
          value: value as string | number,
        });
      }

      if (config.parameters['hyper_parameter_tuning']) {
        m.hyperParameterTuning = {
          iterations: config.parameters['n_iter'],
          selectedTuningMethod: config.parameters['hyper_parameter_tuning'],
          parameters: [],
        };
        for (let [key, value] of Object.entries(
          config.parameters['search_space']
        )) {
          m.hyperParameterTuning.parameters.push({
            name: key,
            value: value as Object,
          });
        }
      }
    }

    if (config.all_categorical === true || config.all_categorical === false) {
      m.all_categorical = config.all_categorical;
    }
    if (config.all_numerical === true || config.all_numerical === false) {
      m.all_numerical = config.all_numerical;
    }
    if (config.threshold) {
      m.threshold = config.threshold;
    }
    return m;
  }
}
