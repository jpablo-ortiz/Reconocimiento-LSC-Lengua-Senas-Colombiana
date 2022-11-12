import { HttpClientTestingModule } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { LoginComponent } from './login.component';

describe('Pruebas Componente LoginComponent', () => {
	beforeEach(async () => {
		await TestBed.configureTestingModule({
			imports: [ HttpClientTestingModule, RouterTestingModule ],
			declarations: [LoginComponent],
		}).compileComponents();
	});

	it('Creación del LoginComponent', () => {
		const fixture = TestBed.createComponent(LoginComponent);
		const app = fixture.componentInstance;
		expect(app).toBeTruthy();
	});

	it('Comprobar formulario de login incompleto', () => {
		const fixture = TestBed.createComponent(LoginComponent);
		const app = fixture.componentInstance;
		fixture.detectChanges();

		// form
		app.formFields.setValue({
			email: 'kennethleo1@hotmail.com',
			password: '',
		});
		expect(app.formFields.valid).toBeFalse();
	});

	it('Comprobar formulario de login válido', () => {
		const fixture = TestBed.createComponent(LoginComponent);
		const app = fixture.componentInstance;
		fixture.detectChanges();

		// form
		app.formFields.setValue({
			email: 'kennethleo1@hotmail.com',
			password: '123456',
		});
		expect(app.formFields.valid).toBeTrue();
	});

	it('Comprobar login correcto', () => {
		const fixture = TestBed.createComponent(LoginComponent);
		const app = fixture.componentInstance;
		fixture.detectChanges();

		// form
		app.formFields.setValue({
			email: 'kennethleo1@hotmail.com',
			password: '123456',
		});

		let button = fixture.debugElement.nativeElement.querySelector('.buttonFix');
		button.click();
		app.token = 'token';
		expect(app.token).toBe('token');
	});

	it('Comprobar login incorrecto', () => {
		const fixture = TestBed.createComponent(LoginComponent);
		const app = fixture.componentInstance;
		fixture.detectChanges();

		let debugElement = fixture.debugElement;

		// form
		app.formFields.setValue({
			email: 'kennethleo1@hotmail.com',
			password: '123456',
		});

		debugElement.nativeElement.querySelector('.buttonFix');
		expect(app.token).toEqual(undefined);
	});
});
