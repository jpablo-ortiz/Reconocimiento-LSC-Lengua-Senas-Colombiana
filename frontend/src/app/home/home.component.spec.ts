// @formatter:off
import 'zone.js';
import 'zone.js/testing';
// @formatter:on
import { TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { HomeComponent } from './home.component';

describe('Pruebas Componente HomeComponent', () => {
	beforeEach(async () => {
		await TestBed.configureTestingModule({
			declarations: [HomeComponent],
		}).compileComponents();
	});

	it('Creación del HomeComponent', () => {
		const fixture = TestBed.createComponent(HomeComponent);
		const app = fixture.componentInstance;
		expect(app).toBeTruthy();
	});

	it('Comprobar título del componente HomeComponent', () => {
		const fixture = TestBed.createComponent(HomeComponent);
		fixture.detectChanges();
		const compiled = fixture.nativeElement;
		expect(compiled.querySelector('h1').textContent).toContain('Manual de uso');
	});

	it('Comprobar existencia apartado integrantes', () => {
		const fixture = TestBed.createComponent(HomeComponent);
		fixture.detectChanges();
		const compiled = fixture.nativeElement;
		expect(compiled.querySelector('h2').textContent).toContain('Grupo de Investigación');
	});

	it('Comprobar existencia información de uno de los integrantes', () => {
		const fixture = TestBed.createComponent(HomeComponent);
		fixture.detectChanges();
		let usuario = fixture.debugElement.query(By.css('.card h3'));
		expect(usuario.nativeElement.textContent).toContain('Juan Pablo Ortiz Rubio');
	});
});
