import { Component, Input } from '@angular/core';
import { ModuleList } from '../workflow-dashboard.model';

@Component({
  selector: 'module-bar',
  templateUrl: './module-bar.component.html',
  styleUrls: ['./module-bar.component.css']
})
export class ModuleBar {
  @Input() modules!: ModuleList;
}
