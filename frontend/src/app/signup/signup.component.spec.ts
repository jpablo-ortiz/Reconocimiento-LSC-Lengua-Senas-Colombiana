// @formatter:off
import 'zone.js';
import 'zone.js/testing';
// @formatter:on
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { SignupComponent } from './signup.component';

describe('Pruebas Componente SignupComponent', () => {
	beforeEach(async () => {
		await TestBed.configureTestingModule({
			imports: [HttpClientTestingModule, RouterTestingModule],
			declarations: [SignupComponent],
		}).compileComponents();
	});

	it('Creación del SignupComponent', () => {
		const fixture = TestBed.createComponent(SignupComponent);
		const app = fixture.componentInstance;
		expect(app).toBeTruthy();
	});

	it('Comprobar formulario de registro incompleto', () => {
		const fixture = TestBed.createComponent(SignupComponent);
		const app = fixture.componentInstance;
		fixture.detectChanges();

		// form
		app.formFields.setValue({
			email: 'kennethleo1@hotmail.com',
			name: 'kenneth',
			role: 'admin',
			password: '',
		});
		expect(app.formFields.valid).toBeFalse();
	});

	it('Comprobar formulario de registro válido', () => {
		const fixture = TestBed.createComponent(SignupComponent);
		const app = fixture.componentInstance;
		fixture.detectChanges();

		// form
		app.formFields.setValue({
			email: 'kennethleo1@hotmail.com',
			name: 'kenneth',
			role: 'admin',
			password: '123456',
		});
		expect(app.formFields.valid).toBeTrue();
	});
});
