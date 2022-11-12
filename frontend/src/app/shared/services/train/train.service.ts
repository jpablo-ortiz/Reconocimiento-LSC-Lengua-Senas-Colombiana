import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';
import { ModelVariables } from '../../models/model-variables/model-variables';
import { Signal } from '../../models/signal/signal';
import { RestService } from '../rest.service';

@Injectable({
	providedIn: 'root',
})
export class TrainService {
	constructor(private restService: RestService) {}

	public trainModel(epochs: number) {
		const url = environment.baseURL + '/train/' + epochs;
		return this.restService.get<any>(url, { headers: this.restService.getHeaders() });
	}

	public getStatusTrainModel() {
		const url = environment.baseURL + '/train-state';
		return this.restService.get<Signal[]>(url, { headers: this.restService.getHeaders() });
	}

	public getTrainingInfo(id_training?: any) {
		let url: string = environment.baseURL + '/training-info';
		if (id_training != null) {
			url += '/' + id_training;
		}
		return this.restService.get<ModelVariables>(url, { headers: this.restService.getHeaders() });
	}

	public getActualModel() {
		const url = environment.baseURL + '/actual-model';
		return this.restService.get<ModelVariables>(url, { headers: this.restService.getHeaders() });
	}
}
