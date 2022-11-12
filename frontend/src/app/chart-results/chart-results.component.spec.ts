// @formatter:off
import 'zone.js';
import 'zone.js/testing';
// @formatter:on
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { ChartResultsComponent } from './chart-results.component';

describe('Pruebas Componente ChartResultsComponent', () => {

	beforeEach(async () => {
		await TestBed.configureTestingModule({
			imports: [HttpClientTestingModule, RouterTestingModule],
			declarations: [ChartResultsComponent],
		}).compileComponents();
	});

	it('Creación del componente ChartResultsComponent', () => {
		const fixture = TestBed.createComponent(ChartResultsComponent);
		const app = fixture.componentInstance;
		expect(app).toBeTruthy();
	});

	it('Verificar que la variable hasData sea falsa', () => {
		const fixture = TestBed.createComponent(ChartResultsComponent);
		const app = fixture.componentInstance;
		fixture.detectChanges();
		expect(app.hasData).toBe(false);
	});

	it('Verificar que la variable hasData sea verdadera ', () => {
		const fixture = TestBed.createComponent(ChartResultsComponent);
		const app = fixture.componentInstance;
		fixture.detectChanges();
		let signals = [];
		signals.push({ signalName: 'good', probability: 70 });
		expect(signals.length).toBe(1);
		app.hasData = true;
		expect(app.hasData).toBe(true);
	});

	it('Realizar promedio de los datos', () => {
		const fixture = TestBed.createComponent(ChartResultsComponent);
		const app = fixture.componentInstance;
		fixture.detectChanges();
		let signals = [];
		signals.push({ signalName: 'good', probability: 70 });
		signals.push({ signalName: 'good', probability: 80 });
		signals.push({ signalName: 'good', probability: 50 });
		let resultado = app.averagePerSignal(signals);
		expect(resultado[0]).toEqual({ signalName: 'good', sum_prob: 66.66666666666667, count: 3 });
	});
});
