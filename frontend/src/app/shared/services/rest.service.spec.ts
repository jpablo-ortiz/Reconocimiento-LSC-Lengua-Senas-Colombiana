import { HttpClientTestingModule } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { RestService } from './rest.service';

describe('Pruebas Servicio RestService', () => {
	let service: RestService;

	beforeEach(() => {
		TestBed.configureTestingModule({
			imports: [RouterTestingModule, HttpClientTestingModule],
		});
		service = TestBed.inject(RestService);
	});

	it('Servicio funcionando correctamente', () => {
		expect(service).toBeTruthy();
	});
});
