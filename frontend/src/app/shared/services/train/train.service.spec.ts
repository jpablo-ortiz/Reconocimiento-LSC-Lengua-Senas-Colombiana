import { HttpClientTestingModule } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { of } from 'rxjs/internal/observable/of';
import { ModelVariables } from '../../models/model-variables/model-variables';
import { Signal } from '../../models/signal/signal';
import { RestService } from '../rest.service';
import { TrainService } from './train.service';

describe('Pruebas Servicio TrainService', () => {
	let service: TrainService;
	let httpClientSpy: { get: jasmine.Spy };

	beforeEach(() => {
		TestBed.configureTestingModule({
			imports: [HttpClientTestingModule],
		});

		httpClientSpy = jasmine.createSpyObj('HttpClient', ['get']);
		service = new TrainService(new RestService(httpClientSpy as any));
	});

	it('Servicio activo correctamente TrainService', () => {
		expect(service).toBeTruthy();
	});

	it('Comprobar retorno arreglo de señas por entrenar', (done: DoneFn) => {
		const resultado = [
			new Signal('Signal 1', [], false),
			new Signal('Signal 2', [], false),
			new Signal('Signal 3', [], false),
		];
		httpClientSpy.get.and.returnValue(of(resultado));

		service.getStatusTrainModel().subscribe((res) => {
			expect(res).toEqual(resultado);
			done();
		});
	});

	it('Comprobar aviso comienzo entrenamiento del modelo', (done: DoneFn) => {
		const epochs = 10;
		const resultado = ['El modelo tiene entrenamiento en proceso'];
		httpClientSpy.get.and.returnValue(of(resultado));

		service.trainModel(epochs).subscribe((res) => {
			expect(res).toEqual(resultado);
			done();
		});
	});

	it('Comprobar retorno estructura de estado del entrenamiento', (done: DoneFn) => {
		const resultado = new ModelVariables(
			1,
			'Entrenamiento 1',
			0.5,
			0.6,
			0.5,
			0.6,
			0.1,
			1,
			60,
			2,
			'2021-05-01 12:00:00',
			'2021-05-01 12:00:00',
			undefined
		);
		httpClientSpy.get.and.returnValue(of(resultado));


		service.getTrainingInfo().subscribe((res) => {
			expect(res).toEqual(resultado);
			done();
		});
	});
});
