import { Component, Input } from '@angular/core';
import {
  ModuleBlueprint,
  ModuleCategory,
} from 'src/app/api/data-preparation/api.service';
import { toPriority } from 'src/app/models/category';

interface CategoryItem {
  name: string;
  icon: string;
  children: ModuleBlueprint[];
  expanded: boolean;
}

@Component({
  selector: 'app-modules-list-nested',
  templateUrl: './modules-list-nested.component.html',
  styleUrls: ['./modules-list-nested.component.css'],
})
export class ModulesListNestedComponent {
  categoryItems: Array<CategoryItem> = [];

  @Input()
  get modules(): Array<ModuleBlueprint> {
    return this._modules;
  }
  set modules(modules: Array<ModuleBlueprint>) {
    this._modules = modules;
    this.categoryItems = this.groupByCategory(modules);
  }
  _modules: Array<ModuleBlueprint>;

  toggleExpand(category: CategoryItem) {
    category.expanded = !category.expanded;
  }

  /**
   * Map flat list of modules to modules grouped by category.
   *
   * Each category has a list of modules.
   *
   * @param modules list of modules.
   * @returns category items with modules as children.
   */
  private groupByCategory(
    modules: Array<ModuleBlueprint>
  ): Array<CategoryItem> {
    const rootNodes: Map<string, CategoryItem> = new Map();
    modules.forEach((m) => {
      if (rootNodes.has(m.category)) {
        const categoryItem = rootNodes.get(m.category);
        categoryItem.children.push(m);
      } else {
        rootNodes.set(m.category, {
          name: m.category,
          icon: this.getIcon(m.category),
          children: [m],
          expanded: false,
        });
      }
    });

    const categoryNodes = Array.from(rootNodes.values());
    const sortedNodes = categoryNodes.sort((a, b) => {
      return toPriority(a.name) - toPriority(b.name);
    });

    return sortedNodes;
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

  getColor(category: string): string {
    switch (category) {
      case 'Filter': {
        return 'type-filter';
      }
      case 'Table': {
        return 'type-table';
      }
      case 'Table-Merge': {
        return 'type-table-merge';
      }
      case 'Preprocess': {
        return 'type-preprocess';
      }
      case 'Visualize': {
        return 'type-visualize';
      }
      case 'Aggregate and Transform': {
        return 'type-aggregate-and-transform';
      }
      default: {
        return '';
      }
    }
  }
}
