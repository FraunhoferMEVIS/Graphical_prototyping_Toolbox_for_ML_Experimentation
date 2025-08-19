import { Component, Input, OnInit } from '@angular/core';


@Component({
  selector: 'app-demo-plot',
  templateUrl: './demo-plot.component.html',
  styleUrls: ['./demo-plot.component.css']
})
export class DemoPlotComponent implements OnInit {

  @Input() plot?: any = "Violin";

  public image: string = "assets/plots/temperature_max_violinplot.png";

  ngOnInit(): void {
    if (this.plot == "Violin") {
      this.image = "assets/plots/temperature_max_violinplot.png";
    } else {
      this.image = "assets/plots/hospital_expire_flag_histogramm.png";
    }
  }
}
