import { ChangeDetectorRef, Component, HostBinding, Input, OnChanges } from '@angular/core';
import { CustomSocket } from './custom-socket';
import { ExecutionState } from '../../models/execution-state';


@Component({
  selector: 'app-custom-socket',
  templateUrl: './custom-socket.component.html',
  styleUrls: ['./custom-socket.component.scss']
})
export class CustomSocketComponent implements OnChanges {
  @Input() data!: CustomSocket;
  @Input() rendered!: any;

  // @HostBinding('class.exported')
  // public get exported(): boolean {
  //   const isOutputWithData = this.data.name == "output" && this.data.moduleInstance?.data.out.length > 0;
  //   const isInputWithData = this.data.name == "input" && this.data.moduleInstance?.data.in.length > 0;
  //   return isInputWithData || isOutputWithData;
  // }

  // @HostBinding('class.exporting')
  // public get exporting(): boolean {
  //   const isOutputAndExporting = this.data.name == "output" && this.data.moduleInstance?.state == ExecutionState.EXECUTING;
  //   return isOutputAndExporting;
  // }

  @HostBinding("title") get title() {
    return this.data.name;
  }

  constructor(private cdr: ChangeDetectorRef) {
    this.cdr.detach();
  }

  ngOnChanges(): void {
    this.cdr.detectChanges();
    requestAnimationFrame(() => this.rendered());
  }

}
