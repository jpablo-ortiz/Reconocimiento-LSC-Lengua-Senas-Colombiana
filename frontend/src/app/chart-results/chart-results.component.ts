import { Component } from '@angular/core';
import { Router } from '@angular/router';
import Swal from 'sweetalert2';

@Component({
	selector: 'app-chart-results',
	templateUrl: './chart-results.component.html',
	styleUrls: ['./chart-results.component.css'],
})
export class ChartResultsComponent {
	// --------------------- VARIABLES ---------------------

	hasData: any = false;
	dataSource: any;
	chartConfig: any;

	// --------------------- CONSTRUCTOR ---------------------

	constructor(private router: Router) {
		if (this.router.getCurrentNavigation() && this.router.getCurrentNavigation()!.extras.state) {
			let signals = this.router.getCurrentNavigation()!.extras.state!['signals'];
			let result = this.averagePerSignal(signals);
			this.hasData = true;

			let adapterList = [];
			for (let j = 0; j < result.length; j++) {
				adapterList.push({
					label: result[j].signalName,
					value: result[j].sum_prob,
				});
			}

			this.chartConfig = {
				width: '80%',
				height: '600',
				type: 'column2d',
				dataFormat: 'json',
			};

			this.dataSource = {
				chart: {
					caption: 'Precisión de la red neuronal',
					xAxisName: 'Seña realizada',
					yAxisName: 'Precisión',
					numberSuffix: '%',
					theme: 'fusion',
				},
				data: adapterList,
			};
		} else {
			this.showErrorNotification();
			setTimeout(() => this.router.navigate(['/translation']), 8000);
		}
	}

	// ---------------------- FUNCTIONS ----------------------

	public averagePerSignal(signals: any[]): any {
		let results: any[] = [];
		// results = [
		// 		{ signalName: 'A', sum_prob: 0, count: 0 },
		// 		{ signalName: 'B', sum_prob: 0, count: 0 },
		// ]

		for (let i = 0; i < signals.length; i++) {
			let signalResult = results.find((result) => result.signalName == signals[i].signalName);

			if (signalResult) {
				signalResult.sum_prob += signals[i].probability;
				signalResult.count++;
			} else {
				results.push({ signalName: signals[i].signalName, sum_prob: signals[i].probability, count: 1 });
			}
		}

		for (let i = 0; i < results.length; i++) {
			results[i].sum_prob = results[i].sum_prob / results[i].count;
		}

		return results;
	}

	// ---------------------- NOTIFICATIONS ----------------------

	public showErrorNotification() {
		Swal.fire({
			icon: 'error',
			title: 'Oops...',
			text: 'No hay datos para mostrar. Redireccionando a la página de traducción...',
			timer: 8000,
		});
	}
}
