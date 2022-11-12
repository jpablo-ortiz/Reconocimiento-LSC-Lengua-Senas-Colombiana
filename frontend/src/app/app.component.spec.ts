// @formatter:off
import 'zone.js';
import 'zone.js/testing';
// @formatter:on
import { TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { AppComponent } from './app.component';

describe('Pruebas Componente AppComponent', () => {
	beforeEach(async () => {
		await TestBed.configureTestingModule({
			imports: [RouterTestingModule],
			declarations: [AppComponent],
		}).compileComponents();
	});

	it('Creación del componente app.component', () => {
		const fixture = TestBed.createComponent(AppComponent);
		const app = fixture.componentInstance;
		expect(app).toBeTruthy();
	});

	it(`Comprobar que el titulo sea 'Reconocimiento LSC'`, () => {
		const fixture = TestBed.createComponent(AppComponent);
		const app = fixture.componentInstance;
		expect(app.title).toEqual('Reconocimiento LSC');
	});

	it(`Comprobar Usuario no logueado`, () => {
		const fixture = TestBed.createComponent(AppComponent);
		const app = fixture.componentInstance;
		expect(app.isLogged).toEqual(false);
	});

	it(`Comprobar nombre de usuario vacío`, () => {
		const fixture = TestBed.createComponent(AppComponent);
		const app = fixture.componentInstance;
		expect(app.username).toEqual('');
	});

	it(`Comprobar item de redirección a otras páginas`, () => {
		const fixture = TestBed.createComponent(AppComponent);
		const app = fixture.componentInstance;
		expect(app.goTo).toBeTruthy();
	});

	it(`Comprobar redirección y creqación componente de login`, () => {
		const fixture = TestBed.createComponent(AppComponent);
		const app = fixture.componentInstance;
		app.goTo('/login');
	});
});
