export enum TrainingState {
	CREATED = 0,
	STARTED = 1,
	PROCESSING = 2,
	FINISHED = 3,
	ERROR = 4,
}

export class ModelVariables {
	public id: number;
	public name: string;
	public loss: number;
	public val_loss: number;
	public accuracy: number;
	public val_accuracy: number;
	public mean_time_execution: number;
	public epoch: number;
	public cant_epochs: number;
	public training_state: TrainingState;
	public begin_time: string;
	public end_time: string;
	public trained_signals: Map<string, string>;

	constructor(
		id?: number,
		name?: string,
		loss?: number,
		val_loss?: number,
		accuracy?: number,
		val_accuracy?: number,
		mean_time_execution?: number,
		epoch?: number,
		cant_epochs?: number,
		training_state?: number,
		begin_time?: string,
		end_time?: string,
		trained_signals?: Map<string, string>
	) {
		this.id = id || 0;
		this.name = name || '';
		this.loss = loss || 0;
		this.val_loss = val_loss || 0;
		this.accuracy = accuracy || 0;
		this.val_accuracy = val_accuracy || 0;
		this.mean_time_execution = mean_time_execution || 0;
		this.epoch = epoch || 0;
		this.cant_epochs = cant_epochs || 0;
		this.training_state = training_state || 0;
		this.begin_time = begin_time || '';
		this.end_time = end_time || '';
		this.trained_signals = trained_signals || new Map<string, string>();

		if (this.begin_time.length > 0) {
			this.begin_time = this.begin_time.replace('T', ' ').substring(0, 19);
		}
		if (this.end_time.length > 0) {
			this.end_time = this.end_time.replace('T', ' ').substring(0, 19);
		}
	}

	public convertTimes() {
		if (this.begin_time.length > 0) {
			this.begin_time = this.begin_time.replace('T', ' ').substring(0, 19);
		}
		if (this.end_time.length > 0) {
			this.end_time = this.end_time.replace('T', ' ').substring(0, 19);
		}
	}

	static empty(): ModelVariables {
		return new ModelVariables();
	}
}
