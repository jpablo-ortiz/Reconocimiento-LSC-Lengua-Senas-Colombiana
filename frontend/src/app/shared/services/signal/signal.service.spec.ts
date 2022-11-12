import { HttpClientTestingModule } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { of } from 'rxjs/internal/observable/of';
import { RestService } from '../rest.service';
import { SignalService } from './signal.service';

describe('Pruebas Servicio SignalService', () => {
	let service: SignalService;
	let httpClientSpy: { post: jasmine.Spy };

	beforeEach(() => {
		TestBed.configureTestingModule({
			imports: [HttpClientTestingModule],
		});

		httpClientSpy = jasmine.createSpyObj('HttpClient', ['post']);
		service = new SignalService(new RestService(httpClientSpy as any));
	});

	it('Servicio activo correctamente SignalService', () => {
		expect(service).toBeTruthy();
	});

	it('Comprobar creación nueva seña', (done: DoneFn) => {
		const signal = {
			name: 'Casa',
			images: ['foto1', 'foto2', 'foto3'],
		};
		const resultado = ['Seña creada correctamente'];
		httpClientSpy.post.and.returnValue(of(resultado));

		const { name, images } = signal;
		service.createSignal(images, name).subscribe((res) => {
			expect(res).toEqual(resultado);
			done();
		});
	});
});
