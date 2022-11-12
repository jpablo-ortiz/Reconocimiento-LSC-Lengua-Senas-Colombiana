// @formatter:off
import 'zone.js';
import 'zone.js/testing';
// @formatter:on
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { NewSignalComponent } from './new-signal.component';

describe('Pruebas Componente NewSignalComponent', () => {
	beforeEach(async () => {
		await TestBed.configureTestingModule({
			imports: [HttpClientTestingModule, RouterTestingModule],
			declarations: [NewSignalComponent],
		}).compileComponents();
	});

	it('Creación del NewSignalComponent', () => {
		const fixture = TestBed.createComponent(NewSignalComponent);
		const app = fixture.componentInstance;
		expect(app).toBeTruthy();
	});

	it('Comprobar arreglo de fotos vacía', () => {
		const fixture = TestBed.createComponent(NewSignalComponent);
		const app = fixture.componentInstance;
		fixture.detectChanges();
		expect(app.processedPhotos.length).toBe(0);
	});

	it('Comprobar la función de vaciar arreglo de fotos capturadas', () => {
		const fixture = TestBed.createComponent(NewSignalComponent);
		const app = fixture.componentInstance;
		fixture.detectChanges();
		app.captures.push('foto1');
		app.captures.push('foto2');
		app.captures.push('foto3');
		expect(app.captures.length).toBe(3);
		app.deleteAll();
		expect(app.captures.length).toBe(0);
	});

	it('Comprobar la función de eliminar foto del arreglo de fotos capturadas', () => {
		const fixture = TestBed.createComponent(NewSignalComponent);
		const app = fixture.componentInstance;
		fixture.detectChanges();
		app.captures.push('foto1');
		app.deletePhoto(0);
		expect(app.captures.length).toBe(0);
	});

	it('Comprobar input de la seña vacío', () => {
		const fixture = TestBed.createComponent(NewSignalComponent);
		const app = fixture.componentInstance;
		fixture.detectChanges();
		expect(app.inputText).toBe('');
	});

	it('Comprobar input de la seña lleno', () => {
		const fixture = TestBed.createComponent(NewSignalComponent);
		const app = fixture.componentInstance;
		fixture.detectChanges();
		app.process();
		app.inputText = 'Hola';
		expect(app.inputText).toBe('Hola');
	});
});
