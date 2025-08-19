export interface Parameter {
  name: string;
  type?: string;
  default?: Object | null | string | number | boolean;
  value?: Object | null | string | number | boolean;
  help?: string;
  options?: string[];
  min?: number;
  max?: number;
  mandatory?: boolean;
}

export interface HyperParameterTuning {
  iterations: number;
  selectedTuningMethod: string;
  parameters: Parameter[];
}

export interface Method {
  step: string;
  name: string;
  parameters: Parameter[];
  hyperParameterTuning?: HyperParameterTuning;
  help?: string;
  ratio?: number[];
  threshold?: number;
  language?: string;
  greater_is_better?: boolean;
  column_name?: string;
  all_numerical?: boolean;
  all_categorical?: boolean;
}
