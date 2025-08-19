import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ModulesListNestedComponent } from './modules-list-nested.component';
import { MatListModule } from '@angular/material/list';
import { MatIconModule } from '@angular/material/icon';
import { MatTooltipModule } from '@angular/material/tooltip';

describe('ModulesListNestedComponent', () => {
  let component: ModulesListNestedComponent;
  let fixture: ComponentFixture<ModulesListNestedComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ModulesListNestedComponent],
      imports: [MatListModule, MatIconModule, MatTooltipModule],
    });
    fixture = TestBed.createComponent(ModulesListNestedComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
