import { HttpErrorResponse } from '@angular/common/http';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { throwError } from 'rxjs';
import { of } from 'rxjs/internal/observable/of';
import { UserService } from './user.service';

describe('Pruebas Servicio UserService', () => {
	let service: UserService;
	let httpClientSpy: { post: jasmine.Spy };

	beforeEach(() => {
		TestBed.configureTestingModule({
			imports: [HttpClientTestingModule],
		});
		httpClientSpy = jasmine.createSpyObj('HttpClient', ['post']);
		service = new UserService(httpClientSpy as any);
	});

	it('Servicio activo correctamente UserService', () => {
		expect(service).toBeTruthy();
	});

	it('Comprobar registro exitoso de un usuario', (done: DoneFn) => {
		const usuarioRegistro = {
			name: 'Kenneth',
			correo: 'kennethleo1@hotmail.com',
			password: '1234',
			role: 'admin',
		};
		const resultado = ['Usuario registrado correctamente'];
		const { name, correo, password, role } = usuarioRegistro;
		httpClientSpy.post.and.returnValue(of(resultado));

		service.signup(name, correo, password, role).subscribe((res) => {
			expect(res).toEqual(resultado);
			done();
		});
	});

	it('Comprobar error de usuario no registrado', (done: DoneFn) => {
		const usuarioRegistro = {
			name: 'Kenneth',
			correo: 'kennethleo1@hotmail.com',
			password: '1234',
			role: 'admin',
		};
		const error = new HttpErrorResponse({
			error: { message: 'Usuario  no registardo' },
			status: 400,
		});
		const { name, correo, password, role } = usuarioRegistro;
		httpClientSpy.post.and.returnValue(throwError(error));

		service.signup(name, correo, password, role).subscribe(
			(res) => {},
			(err) => {
				expect(err).toEqual(error);
				done();
			}
		);
	});

	it('Comprobar datos del usuario retornados', (done: DoneFn) => {
		const usuarioLogin = {
			email: 'kennethleo1@hotmail.com',
			contra: '1234',
		};
		const resultado = {
			role: 'admin',
			usuario: 'Kenneth',
			token: 'DevuelveUnToken',
		};
		const { email, contra } = usuarioLogin;
		httpClientSpy.post.and.returnValue(of(resultado));

		service.login(email, contra).subscribe((res) => {
			expect(res).toEqual(resultado);
			done();
		});
	});

	it('Comprobar retorno de error de falta credenciales del usuario', (done: DoneFn) => {
		const usuarioLogin = {
			email: '	kennethleo1@hotmail.com',
			contra: '',
		};
		const error = new HttpErrorResponse({
			error: { message: 'Usuario invalido' },
			status: 400,
		});
		const { email, contra } = usuarioLogin;
		httpClientSpy.post.and.returnValue(throwError(error));

		service.login(email, contra).subscribe(
			(res) => {},
			(err) => {
				expect(err).toEqual(error);
				done();
			}
		);
	});
});
