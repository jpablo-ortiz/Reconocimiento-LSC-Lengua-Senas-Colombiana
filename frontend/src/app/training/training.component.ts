import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import Swal from 'sweetalert2';
import { ModelVariables, TrainingState } from '../shared/models/model-variables/model-variables';
import { Signal } from '../shared/models/signal/signal';
import { TrainService } from '../shared/services/train/train.service';

@Component({
	selector: 'app-training',
	templateUrl: './training.component.html',
	styleUrls: ['./training.component.css'],
})
export class TrainingComponent implements OnInit {
	// --------------------- VARIABLES ---------------------

	// Form variables
	epochs: number = 1000;

	// Actual Model
	actualModel: ModelVariables = ModelVariables.empty();
	get alistSignsActualModel(): string[] {
		// Convert map actualModel.trained_signals to array
		return Object.values(this.actualModel.trained_signals);
	}

	// Training info
	trainingInfo: ModelVariables = ModelVariables.empty();
	trainingChangesListener: any;

	// Timer variables
	viewCountdown: boolean = false;
	secondsCountdown: number = 0;
	countdown: string = '00:00:00';

	// Processing signs
	processingSigns: boolean = false;

	// HTML Elements
	trainingButton: any;

	// --------------------- CONSTRUCTOR ---------------------

	constructor(private trainService: TrainService, private router: Router) {}

	// ------------------- NgOn FUNCTIONS --------------------

	ngOnInit(): void {
		// Init components
		this.trainingButton = document.getElementById('button_train');
		this.trainingButton.disabled = true;

		// Get actual model
		this.getActualModel();

		// Get training info
		this.getTrainingInfo();

		// Define Listeners
		this.trainingButton.addEventListener('click', () => this.startTraining());
	}

	ngOnDestroy() {
		// Remove listeners
		clearInterval(this.trainingChangesListener);
	}

	// ---------------------- FUNCTIONS ----------------------

	private getActualModel() {
		this.trainService.getActualModel().subscribe((model: ModelVariables) => (this.actualModel = model));
	}

	private getTrainingInfo() {
		this.trainService.getTrainingInfo().subscribe(
			(train: ModelVariables) => {
				if (train.training_state! == TrainingState.FINISHED || train.training_state! == TrainingState.ERROR) {
					// Verify if a signal is not trained
					this.verifyNotTrainedSigns();
				} else {
					// A Training is running
					this.trainingButton.disabled = true;

					// Init listener of training changes
					this.trainingChangesListener = setInterval(() => this.getTrainingChanges(), 5000);

					this.onProgressNotification();
				}
			},
			(_err) => {
				this.errorInternalServerNotification();
			}
		);
	}

	private verifyNotTrainedSigns() {
		this.trainService.getStatusTrainModel().subscribe(
			(notTrainedSigns) => {
				if (notTrainedSigns.length > 0) {
					this.trainingButton.disabled = false;
					this.newSignalsToTrainNotification(notTrainedSigns);
				} else {
					this.notNecessaryTrainNotification();
				}
			},
			(err) => {
				this.errorGetingTrainingInfoNotification(err);
			}
		);
	}

	private startTraining() {
		this.trainingButton.disabled = true;
		this.trainService.trainModel(this.epochs).subscribe(
			(_res) => {
				this.trainingStartingNotification();

				// Init listener of training changes
				this.trainingChangesListener = setInterval(() => this.getTrainingChanges(), 5000);
			},
			(_err) => {
				this.errorStartingTrainingNotification();
				this.trainingButton.disabled = false;
			}
		);
	}

	private getTrainingChanges() {
		this.trainService.getTrainingInfo().subscribe((train: ModelVariables) => {
			train.begin_time = train.begin_time.replace('T', ' ').substring(0, 19);
			this.trainingInfo = train;

			switch (this.trainingInfo.training_state!) {
				case TrainingState.CREATED:
					// Message processing signals before start training
					this.processingSigns = true;
					break;

				case TrainingState.STARTED:
				case TrainingState.PROCESSING:
					// Change seconds of timer to seconds of actual training
					this.secondsCountdown =
						this.trainingInfo.mean_time_execution *
						(this.trainingInfo.cant_epochs - this.trainingInfo.epoch);

					// If Countdown is not started, start it
					this.initCountdown();
					break;

				case TrainingState.FINISHED:
					// Stop training changes listener
					clearInterval(this.trainingChangesListener!);
					this.secondsCountdown = 0;

					this.trainingFinishedNotification();

					// sleep 4 seconds
					setTimeout(() => {
						this.router.navigate(['/translation']);
					}, 4000);
					break;

				case TrainingState.ERROR:
					// Stop training changes listener
					clearInterval(this.trainingChangesListener!);
					this.secondsCountdown = 0;

					this.errorTrainingNotification();
					this.trainingButton.disabled = false;
					break;

				default:
					// Stop training changes listener
					clearInterval(this.trainingChangesListener!);
			}
		});
	}

	private initCountdown() {
		if (!this.viewCountdown) {
			// Deactivate processing signs
			this.processingSigns = false;
			// Countdown interval init
			setInterval(() => {
				if (this.secondsCountdown > 1) {
					this.secondsCountdown--;
				}
				// Convert seconds to hours, minutes and seconds string
				this.countdown = new Date(this.secondsCountdown * 1000).toISOString().substring(11, 19);
			}, 1000);
			this.viewCountdown = true;
		}
	}

	// ---------------------- NOTIFICATIONS ----------------------

	public newSignalsToTrainNotification(notTrainedSigns: Signal[]) {
		// Make a list of not trained signs names
		let notTrainedSignsNames: string[] = [];
		notTrainedSigns.forEach((sign) => {
			notTrainedSignsNames.push(sign.name);
		});

		// Show a message with the list of not trained signs
		let stringNotTrainedSigns = notTrainedSignsNames.join(', ');

		Swal.fire({
			icon: 'success',
			title: 'Señas por entrenar',
			text: 'Se han encontrado señas por entrenar en el sistema:\n' + '[' + stringNotTrainedSigns + ']',
		});
	}

	private onProgressNotification() {
		Swal.fire({
			icon: 'info',
			title: 'Entrenamiento en proceso',
			text: 'Hay un entrenamiento en proceso',
			timer: 5000,
		});
	}

	public errorGetingTrainingInfoNotification(error: any) {
		Swal.fire({
			icon: 'error',
			title: 'Error al obtener información del entrenamiento.',
			text: 'Error Interno del Servidor: \n' + error.error.detail,
			timer: 5000,
		});
	}

	public notNecessaryTrainNotification() {
		Swal.fire({
			icon: 'warning',
			title: 'Tranquilo todo esta entrenado',
			text: 'No se han encontrado señas por entrenar en el sistema. \n Captura nuevas señas para entrenar el modelo',
		});
	}

	public trainingStartingNotification() {
		Swal.fire({
			icon: 'success',
			title: 'Inicio de procesamiento',
			text: 'Se ha iniciado el procesamiento de las señas.',
		});
	}

	public errorStartingTrainingNotification() {
		Swal.fire({
			icon: 'error',
			title: 'Error al entrenar el modelo',
			text: 'Ha ocurrido un error al entrenar el modelo, por favor intente de nuevo.',
		});
	}

	public trainingFinishedNotification() {
		Swal.fire({
			icon: 'success',
			title: 'Entrenamiento finalizado',
			text: 'El modelo se ha entrenado correctamente',
		});
	}

	public errorTrainingNotification() {
		Swal.fire({
			icon: 'error',
			title: 'Entrenamiento fallido',
			text: 'El modelo no se ha podido entrenar.',
		});
	}

	public errorInternalServerNotification() {
		Swal.fire({
			icon: 'error',
			title: 'Error del servidor',
			text: 'Ha ocurrido un error en el servidor, por favor intente de nuevo.',
		});
	}
}
