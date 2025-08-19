import { Component, OnInit, Input, OnDestroy } from '@angular/core';
import { MethodSelectionService } from '../../services/method-selection.service';
import { Observable, Subscription, first } from 'rxjs';
import { blendInOut } from '../../animations';
import { AddAlgorithmDialogComponent } from './add-algorithm-dialog/add-algorithm-dialog.component';
import { Method } from 'src/app/models/method';
import { MatDialog } from '@angular/material/dialog';
import { Steps } from 'src/app/backend-client';
import { Filters } from 'src/app/backend-client';
import { FormControl } from '@angular/forms';
import { MethodsService } from 'src/app/backend-client';

type Layout = 'list' | 'grid';

@Component({
  selector: 'app-algorithms',
  templateUrl: './algorithms.component.html',
  styleUrls: ['./algorithms.component.scss'],
  animations: [blendInOut],
})
export class AlgorithmSelectionComponent implements OnInit, OnDestroy {
  @Input() public step: Steps = '';
  @Input() public optionsObservable$: Observable<any> = new Observable<any>();
  @Input() public specificFormGroup: any;
  @Input() public preAppliedFilters?: string[] = [];
  public filters: FormControl = new FormControl([]);
  public possibleFilters: Filters[] = [];
  public filteredOptions: string[] = [];
  public allOptions: string[] = [];

  public layout: Layout = 'list';
  public breakpoint: number = 4;
  private readonly breakpointThresholdPx: number = 900;

  private optionsSubscription: Subscription = new Subscription();
  private searchValueSubscription: Subscription = new Subscription();
  private selectedFiltersSubscription: Subscription = new Subscription();
  private possibleFiltersSubscription: Subscription = new Subscription();

  constructor(
    public methodSelectionService: MethodSelectionService,
    public methodsService: MethodsService,
    public dialog: MatDialog
  ) {}

  ngOnInit(): void {
    this.breakpoint = this.calculateBreakpoint(window.innerWidth);

    this.createOptionsSubscription();
    this.selectedFiltersSubscription = this.filters.valueChanges.subscribe(
      (c) => {
        this.optionsSubscription?.unsubscribe();
        this.optionsObservable$ =
          this.methodSelectionService.setObservableForStep(
            this.step,
            c[0] as Filters
          );
        this.createOptionsSubscription();
      }
    );
    this.searchValueSubscription = this.methodSelectionService
      .getSearchValueChange()
      .subscribe((c) => {
        this.applySearch();
      });
    this.possibleFiltersSubscription = this.methodsService
      .getFiltersOfStepMethodsStepFiltersStepGet(this.step)
      .subscribe((f) => {
        this.possibleFilters = f;
        if (
          this.preAppliedFilters &&
          this.preAppliedFilters.filter((f) => f != '' && f != null).length > 0
        ) {
          this.filters.setValue(
            this.preAppliedFilters.filter((f) =>
              this.possibleFilters.includes(f as Filters)
            )
          );
        }
      });
  }

  onResize(event: any) {
    this.breakpoint = this.calculateBreakpoint(event.target.innerWidth);
  }

  /**
   * Calculates based on width how many columns to display in grid view.
   *
   * @param width of window.
   * @returns number of columns to display.
   */
  private calculateBreakpoint(width: number) {
    return width <= this.breakpointThresholdPx ? 1 : 4;
  }

  public createOptionsSubscription(): void {
    this.optionsSubscription = this.optionsObservable$.subscribe((o) => {
      this.allOptions = o.algorithms[0].algorithms.sort();
      this.filteredOptions = this.allOptions;
      this.applySearch();
    });
  }

  ngOnDestroy(): void {
    this.optionsSubscription?.unsubscribe();
    this.searchValueSubscription?.unsubscribe();
    this.selectedFiltersSubscription?.unsubscribe();
    this.possibleFiltersSubscription?.unsubscribe();
  }

  openDialog(name: string): void {
    this.methodSelectionService
      .getMethodWithName(name, this.step)
      .pipe(first())
      .subscribe((d) => {
        const dialogRef = this.dialog.open(AddAlgorithmDialogComponent, {
          data: d,
          maxWidth: '60vw',
        });

        dialogRef
          .afterClosed()
          .pipe(first())
          .subscribe((result) => {
            if (result && result.event == 'cancel') {
            } else if (result && result.event == 'submit') {
              this.selectOption(result.data);
            }
          });
      });
  }

  /**
   * Filters the list of options based on the search value entered by the user.
   */
  private applySearch() {
    // Get the search value from the form control
    const searchValue =
      this.methodSelectionService.generalFormGroup.controls.search.value;

    // If a search value is present, filter the options based on the search value
    if (searchValue) {
      this.filteredOptions = this.allOptions.filter((algorithm) =>
        algorithm.toLowerCase().includes(searchValue.toLowerCase())
      );
    }
    // If no search value is present, show all options
    else {
      this.filteredOptions = this.allOptions;
    }
  }

  public selectOption(option: Method) {
    (this.specificFormGroup.controls.selectedOptions.value! as Method[]).push(
      option
    );
  }
}
