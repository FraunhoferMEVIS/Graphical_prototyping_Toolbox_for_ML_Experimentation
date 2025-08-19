import {
  AfterViewInit,
  Component,
  DestroyRef,
  ViewChild,
  inject,
} from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { DashboardService } from 'src/app/workflow-dashboard/workflow-dashboard.service';
import { NewProjectDialogComponent } from '../new-project-dialog/new-project-dialog.component';
import { MatTableDataSource } from '@angular/material/table';
import { MatSort } from '@angular/material/sort';
import { MatPaginator } from '@angular/material/paginator';
import { SelectionModel } from '@angular/cdk/collections';
import { ActionDialogComponent } from '../action-dialog/action-dialog.component';
import { mergeMap, of } from 'rxjs';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { EditProjectDialogComponent } from '../edit-project-dialog/edit-project-dialog.component';

/**
 * Represents a project within the table.
 */
interface ProjectItem {
  name: string;
}

@Component({
  selector: 'app-project-list',
  templateUrl: './project-list.component.html',
  styleUrls: ['./project-list.component.css'],
})
export class ProjectListComponent implements AfterViewInit {
  @ViewChild(MatSort) sort: MatSort;
  @ViewChild(MatPaginator) paginator: MatPaginator;

  destroyRef = inject(DestroyRef);

  displayedColumns: string[] = ['name', 'actions'];
  dataSource: MatTableDataSource<ProjectItem>;
  selection: SelectionModel<ProjectItem>;
  selectionEnabled = false;

  constructor(
    public dashboardService: DashboardService,
    private dialog: MatDialog
  ) {
    const initialSelection = [];
    const allowMultiSelect = false;
    this.selection = new SelectionModel<ProjectItem>(
      allowMultiSelect,
      initialSelection
    );

    this.dataSource = new MatTableDataSource([]);
    this.subscribeToProjects();
  }

  subscribeToProjects() {
    return this.dashboardService.projects$
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe((projects) => {
        const convertedItems = projects.map((p) => {
          return { name: p };
        });
        this.dataSource.data = convertedItems;
      });
  }

  ngAfterViewInit() {
    this.dataSource.sort = this.sort;
    this.dataSource.paginator = this.paginator;
  }

  editProject(index: number, event: MouseEvent) {
    const realIndex =
      index + this.paginator.pageIndex * this.paginator.pageSize;
    const project = this.dataSource.data[realIndex];

    this.dialog
      .open(EditProjectDialogComponent, {
        data: { title: 'Edit Project', currentProject: project.name },
      })
      .afterClosed()
      .pipe(
        takeUntilDestroyed(this.destroyRef),
        mergeMap((success) => {
          if (success) {
            return this.dashboardService.loadProjects();
          } else {
            return of();
          }
        })
      )
      .subscribe();
  }

  deleteProject(index: number, event: MouseEvent) {
    const realIndex =
      index + this.paginator.pageIndex * this.paginator.pageSize;
    const project = this.dataSource.data[realIndex];
    this.dialog
      .open(ActionDialogComponent, {
        data: {
          title: `Are you sure you want to continue?`,
          description: `The project ${project.name} will be deleted.`,
        },
      })
      .afterClosed()
      .pipe(
        mergeMap((confirm: boolean) => {
          if (confirm) {
            return this.dashboardService.deleteProject(project.name);
          } else {
            return of(false);
          }
        }),
        mergeMap(() => this.dashboardService.loadProjects()),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe();
  }

  createProject() {
    this.dialog
      .open(NewProjectDialogComponent, {
        data: { title: 'New Project' },
      })
      .afterClosed()
      .pipe(
        takeUntilDestroyed(this.destroyRef),
        mergeMap((success) => {
          if (success) {
            return this.dashboardService.loadProjects();
          } else {
            return of();
          }
        })
      )
      .subscribe();
  }

  selectProject(project: ProjectItem) {
    if (!this.selectionEnabled) {
      return;
    }

    if (this.selection.isSelected(project)) {
      this.selection.deselect(project);
    } else {
      this.selection.select(project);
    }
  }
}
