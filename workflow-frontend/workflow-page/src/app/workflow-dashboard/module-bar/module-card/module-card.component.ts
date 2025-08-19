import { Component, Input } from '@angular/core';
import { Module } from '../../models/module';

@Component({
  selector: 'module-card',
  templateUrl: './module-card.component.html',
  styleUrls: ['./module-card.component.css'],
})
export class ModuleCard {
    @Input() module!: Module
}
