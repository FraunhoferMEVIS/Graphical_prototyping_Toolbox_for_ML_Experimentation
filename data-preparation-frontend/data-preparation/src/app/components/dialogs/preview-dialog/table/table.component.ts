import { Component, DestroyRef, Input, OnInit } from '@angular/core';
import { TableService } from '../../../../services/table.service';
import { MatTableDataSource } from '@angular/material/table';
import { ModuleInstance } from 'src/app/models/network';
import { Column } from 'src/app/api/data-preparation/api.service';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { NotificationService } from 'src/app/services/notification.service';

const MESSAGES = {
  NO_DATA_AVAILABLE: 'No output table available for this module',
  EMPTY_DATASET: 'The output table is empty',
  NO_MORE_DATA_AVAILBLE: 'No more data available',
};

@Component({
  selector: 'app-table',
  templateUrl: './table.component.html',
  styleUrls: ['./table.component.css'],
})
export class TableComponent implements OnInit {
  @Input() moduleInstance: ModuleInstance;
  columns: Column[] = [];

  Number = Number;
  tableDataSource = new MatTableDataSource<any>([]);

  // paging parameters
  start: number = 0;
  limit: number = 30;
  end: number = this.limit + this.start;

  // component state flags
  reachedEnd: boolean = false;
  loading: boolean = false;

  errorMessage: string = MESSAGES.NO_DATA_AVAILABLE;

  constructor(
    private tableService: TableService,
    private destroyRef: DestroyRef,
    private notificationService: NotificationService
  ) {}

  ngOnInit(): void {
    this.getTableData(this.start, this.limit, true);
  }

  noDataAvailable(): boolean {
    return (
      this.reachedEnd &&
      this.tableDataSource.data.length == 0 &&
      this.columns.length == 0
    );
  }

  getTableData(start: number, end: number, initial: boolean = false) {
    this.loading = true;

    this.tableService
      .getData(this.moduleInstance.module.id, start / this.limit, end - start)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe({
        next: ({ data, error }) => {
          const tablePage = data;

          if (error) {
            this.reachedEnd = true;
            this.errorMessage = MESSAGES.NO_DATA_AVAILABLE;
            if (!initial) {
              this.notificationService.showInfo(MESSAGES.NO_MORE_DATA_AVAILBLE);
            }

            return;
          }

          if (initial) {
            this.tableDataSource = new MatTableDataSource(tablePage.data);
            this.columns = tablePage.columns;

            if (data.data.length == 0) {
              this.reachedEnd = true;
            }
          } else {
            if (data.data.length == 0) {
              this.reachedEnd = true;
              this.notificationService.showInfo(MESSAGES.NO_MORE_DATA_AVAILBLE);
            } else {
              this.tableDataSource.data = this.tableDataSource.data.concat(
                tablePage.data
              );
            }
          }

          this.updateIndex();
        },
        error: (err) => {
          console.error(err);
          this.notificationService.showError('Failed to fetch table data');
          this.loading = false;
        },
        complete: () => {
          this.loading = false;
        }
      });
  }

  onTableScroll(e) {
    if (this.reachedEnd || this.loading) {
      return;
    }

    const tableViewHeight = e.target.offsetHeight; // viewport
    const tableScrollHeight = e.target.scrollHeight; // length of all table
    const scrollLocation = e.target.scrollTop; // how far user scrolled

    // If the user has scrolled within 200px of the bottom, add more data
    const buffer = 200;
    const limit = tableScrollHeight - tableViewHeight - buffer;
    if (scrollLocation > limit) {
      this.getTableData(this.start, this.end);
    }
  }

  updateIndex() {
    this.start = this.end;
    this.end = this.limit + this.start;
  }

  getColumnNames(columns: Array<Column>): string[] {
    if (columns == null) {
      return [];
    }

    return columns.map((c) => c.name);
  }
}
