import { TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { WebsocketService } from './websocket.service';

describe('Pruebas Servicio WebsocketService', () => {
	let service: WebsocketService;

	beforeEach(() => {
		TestBed.configureTestingModule({
			imports: [RouterTestingModule],
		});
		service = TestBed.inject(WebsocketService);
	});

	it('Servicio funcionando correctamente', () => {
		expect(service).toBeTruthy();
	});
});
