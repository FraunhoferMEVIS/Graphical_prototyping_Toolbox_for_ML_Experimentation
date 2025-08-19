import { Component, Input } from '@angular/core';
import {
  ModuleBlueprint,
  ModuleCategory,
} from 'src/app/api/data-preparation/api.service';

export interface ModuleItem {
  module: ModuleBlueprint;
  fontIcon: string;
}

@Component({
  selector: 'app-modules-list',
  templateUrl: './modules-list.component.html',
  styleUrls: ['./modules-list.component.css'],
})
export class ModulesListComponent {
  title = 'Available Modules';
  moduleItems: Array<ModuleItem> = [];

  @Input()
  get modules(): Array<ModuleBlueprint> {
    return this._modules;
  }
  set modules(modules: Array<ModuleBlueprint>) {
    this._modules = modules;
    this.moduleItems = this.toModuleItem(modules);
  }
  _modules: Array<ModuleBlueprint>;

  private toModuleItem(modules: Array<ModuleBlueprint>): Array<ModuleItem> {
    return modules.map((m) => {
      return {
        module: m,
        fontIcon: this.getIcon(m.category),
      };
    });
  }

  private getIcon(moduleType: ModuleCategory): string {
    switch (moduleType) {
      case 'Filter': {
        return 'filter_alt';
      }
      case 'Table': {
        return 'table_view';
      }
      case 'Table-Merge': {
        return 'call_merge';
      }
      case 'Preprocess': {
        return 'science';
      }
      case 'Visualize': {
        return 'scatter_plot';
      }
      case 'Aggregate and Transform': {
        return 'transform';
      }
      default: {
        return '';
      }
    }
  }
}
