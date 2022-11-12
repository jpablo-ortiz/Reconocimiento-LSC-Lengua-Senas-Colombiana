// @formatter:off
import 'zone.js';
import 'zone.js/testing';
// @formatter:on
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { RouterTestingModule } from '@angular/router/testing';
import { TrainingComponent } from './training.component';

describe('Pruebas Componente TrainingComponent', () => {
	beforeEach(async () => {
		await TestBed.configureTestingModule({
			imports: [HttpClientTestingModule, RouterTestingModule],
			declarations: [TrainingComponent],
		}).compileComponents();
	});

	it('Creación del componente TrainingComponent', () => {
		const fixture = TestBed.createComponent(TrainingComponent);
		const app = fixture.componentInstance;
		expect(app).toBeTruthy();
	});

	it('Comprobar botón de entrenamiento deshabilitado', () => {
		const fixture = TestBed.createComponent(TrainingComponent);
		const app = fixture.componentInstance;
		fixture.detectChanges();

		let button = fixture.debugElement.query(By.css('#button_train'));
		expect(button.nativeElement.disabled).toBeTrue();
	});

	it('Comprobar modelo actual este vació', () => {
		const fixture = TestBed.createComponent(TrainingComponent);
		const app = fixture.componentInstance;
		fixture.detectChanges();

		expect(app.actualModel.id).toBe(0);
		expect(app.actualModel.name).toBe('');
		expect(app.actualModel.loss).toBe(0);
		expect(app.actualModel.val_loss).toBe(0);
		expect(app.actualModel.accuracy).toBe(0);
		expect(app.actualModel.val_accuracy).toBe(0);
		expect(app.actualModel.mean_time_execution).toBe(0);
		expect(app.actualModel.epoch).toBe(0);
		expect(app.actualModel.cant_epochs).toBe(0);
		expect(app.actualModel.training_state).toBe(0);
		expect(app.actualModel.begin_time).toBe('');
		expect(app.actualModel.end_time).toBe('');
		expect(app.actualModel.trained_signals.size).toBe(0);
	});
});
