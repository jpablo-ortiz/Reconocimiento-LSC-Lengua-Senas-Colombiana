import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { RestService } from '../rest.service';

@Injectable({
	providedIn: 'root',
})
export class SignalService {
	constructor(private restService: RestService) {}

	public createSignal(arreglo: any, nombreSena: string) {
		const url = environment.baseURL + '/new-signal';
		return this.restService.post<any>(
			url,
			{
				name: nombreSena,
				images: arreglo,
			},
			{ headers: this.restService.getHeaders() }
		);
	}
}
