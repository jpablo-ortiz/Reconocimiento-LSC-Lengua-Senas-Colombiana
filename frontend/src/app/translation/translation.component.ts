import { Component, OnInit, Renderer2 } from '@angular/core';
import { NavigationExtras, Router } from '@angular/router';

import { Camera } from '@mediapipe/camera_utils';
import { drawConnectors, drawLandmarks } from '@mediapipe/drawing_utils/';
import { HAND_CONNECTIONS, Holistic, POSE_CONNECTIONS } from '@mediapipe/holistic';
import { fromEvent, Observable, Subscription } from 'rxjs';
import { WebSocketSubject } from 'rxjs/webSocket';
import { WebsocketService } from '../shared/services/signal/websocket.service';

@Component({
	selector: 'app-translation',
	templateUrl: './translation.component.html',
	styleUrls: ['./translation.component.css'],
	providers: [WebsocketService],
})
export class TranslationComponent implements OnInit {
	// --------------------- VARIABLES ---------------------

	// Flags
	initializated: any = false;

	// HTML Elements
	videoElement: any;
	buttonChartResults: HTMLElement | any;
	audioCheckbox: any;

	canvasElement: any;
	canvasCtx: any;

	// MediaPipe
	camera: Camera | any;
	actualHolisticCoords: any;

	// Server connection variables
	signalPredicted: any;
	messageInterval = 1000;
	bestSignalsPerPrediction: any[] = [];

	// Listeners, subscriptions and observables
	resizeObservable?: Observable<Event>;
	resizeSubscription?: Subscription;
	captureInterval: any;

	// --------------------- CONSTRUCTOR ---------------------

	constructor(private websocketService: WebsocketService, private router: Router, private renderer: Renderer2) {
		let processingWSMessages = (msg: any, ws: WebSocketSubject<any>) => {
			var mensaje = JSON.parse(msg);
	
			// Transform json message to array of signals
			let receivedSignals = [];
			for (let key in mensaje) {
				receivedSignals.push({ signalName: key, probability: mensaje[key] });
			}

			// Save the best signals of the prediction
			this.bestSignalsPerPrediction.push(receivedSignals[0]);
	
			// clean the array always leaving the last 30 signals
			if (this.bestSignalsPerPrediction.length == 30) {
				this.bestSignalsPerPrediction.shift();
			}
	
			// If the list has more than 1 signal, we can show the chart results
			if (this.bestSignalsPerPrediction.length > 1) {
				this.buttonChartResults.disabled = false;
				this.buttonChartResults.setAttribute('class', 'btn btn-primary');
			} else {
				this.buttonChartResults.disabled = true;
				this.buttonChartResults.setAttribute('class', 'btn btn-secondary');
			}
	
			// Print the signals on the screen
			if (receivedSignals[0].probability >= 95 || receivedSignals.length == 1) {
				if (receivedSignals[0].signalName === 'Sabado') {
					this.signalPredicted = 'Sábado';
				} else if (receivedSignals[0].signalName === 'Telefono') {
					this.signalPredicted = 'Teléfono';
				} else if (receivedSignals[0].signalName === 'Balon') {
					this.signalPredicted = 'Balón';
				} else if (receivedSignals[0].signalName === 'Lampara') {
					this.signalPredicted = 'Lámpara';
				} else {
					this.signalPredicted = receivedSignals[0].signalName;
				}
			} else {
				this.signalPredicted = receivedSignals[0].signalName;
				this.signalPredicted += '<br>' + '<br>';
				this.signalPredicted += 'Otras posibles señas son: ';
				this.signalPredicted += '<br>';
				this.signalPredicted += receivedSignals[1].signalName;
				if (receivedSignals.length > 2) {
					this.signalPredicted += '<br>';
					this.signalPredicted += receivedSignals[2].signalName;
				}
			}
	
			// Play audio if the audio checkbox is checked
			if (this.audioCheckbox.checked) {
				speechSynthesis.cancel();
				this.playAudio(this.signalPredicted);
			}
		}
		websocketService.getMessages(processingWSMessages);
		this.captureInterval = setInterval(() => this.sendMessage(), this.messageInterval);
	}

	// ------------------- NgOn FUNCTIONS --------------------

	ngOnInit() {
		// Get the buttonChartResults element
		this.buttonChartResults = document.getElementById('buttonChartResults');
		this.buttonChartResults.disabled = true;
		this.buttonChartResults.setAttribute('class', 'btn btn-secondary');
		this.buttonChartResults.addEventListener('click', () => {
			let navigationExtras: NavigationExtras = {
				state: {
					signals: this.bestSignalsPerPrediction,
				},
			};
			this.router.navigate(['/chart-results'], navigationExtras);
		});

		// Get the audio checkbox element
		this.audioCheckbox = document.getElementsByClassName('sound')[0];
		this.audioCheckbox.checked = false;
		this.audioCheckbox.addEventListener('change', () => {
			this.setMessageInterval(this.audioCheckbox.checked);
		});

		// Get the video and canvas element
		this.videoElement = document.getElementsByClassName('input_video')[0];
		this.canvasElement = document.getElementsByClassName('output_canvas')[0];
		this.canvasCtx = this.canvasElement.getContext('2d');

		// Initialize listener to resize canvas when window is resized
		let canvaHeight = this.canvasElement.clientWidth * 0.75;
		this.renderer.setStyle(this.canvasElement, 'height', `${canvaHeight}px`);
		this.resizeObservable = fromEvent(window, 'resize');
		this.resizeSubscription = this.resizeObservable.subscribe((evt) => {
			let canvaHeight = this.canvasElement.clientWidth * 0.75;
			if (canvaHeight < 1000) {
				this.renderer.setStyle(this.canvasElement, 'width', '100%');
			}
			this.renderer.setStyle(this.canvasElement, 'height', `${canvaHeight}px`);

			if (this.canvasElement.clientWidth > 1330) {
				this.renderer.setStyle(this.canvasElement, 'width', '1330px');
			}
		});

		// MediaPipe Holistic detection
		const holistic = new Holistic({
			locateFile: (file) => {
				return `https://cdn.jsdelivr.net/npm/@mediapipe/holistic/${file}`;
			},
		});
		holistic.setOptions({
			modelComplexity: 1,
			smoothLandmarks: true,
			enableSegmentation: true,
			smoothSegmentation: true,
			refineFaceLandmarks: true,
			minDetectionConfidence: 0.5,
			minTrackingConfidence: 0.5,
		});

		this.camera = new Camera(this.videoElement, {
			onFrame: async () => {
				await holistic.send({ image: this.videoElement });
				this.initializated = true;
			},
		});

		this.camera.start();
		this.setMessageInterval(this.audioCheckbox.checked);
		holistic.onResults(this.printAndGetHolisticResult.bind(this));
	}

	ngOnDestroy() {
		this.resizeSubscription?.unsubscribe();
		clearInterval(this.captureInterval);
		speechSynthesis.cancel();
		this.camera.stop();
	}

	// ---------------------- FUNCTIONS ----------------------

	public printAndGetHolisticResult(results: any) {
		this.canvasCtx.save();
		this.canvasCtx.clearRect(0, 0, this.canvasElement.width, this.canvasElement.height);

		// Only overwrite existing pixels.
		this.canvasCtx.globalCompositeOperation = 'source-in';

		this.canvasCtx.fillStyle = 'rgba(0,0,0,0.2)';
		this.canvasCtx.fillRect(0, 0, this.canvasElement.width, this.canvasElement.height);

		// Only overwrite missing pixels.
		this.canvasCtx.globalCompositeOperation = 'destination-atop';
		this.canvasCtx.drawImage(results.image, 0, 0, this.canvasElement.width, this.canvasElement.height);
		this.canvasCtx.globalCompositeOperation = 'source-over';

		// POSE
		drawConnectors(this.canvasCtx, results.poseLandmarks, POSE_CONNECTIONS, { color: '#00FF00', lineWidth: 0.2 });
		drawLandmarks(this.canvasCtx, results.poseLandmarks, {
			color: '#FF0000',
			lineWidth: 0,
			radius: 0.2,
		});

		// LEFT HAND
		drawConnectors(this.canvasCtx, results.leftHandLandmarks, HAND_CONNECTIONS, {
			color: '#FFFFFF',
			lineWidth: 0.4,
		});
		drawLandmarks(this.canvasCtx, results.leftHandLandmarks, {
			color: '#FF0000',
			lineWidth: 0.4,
			radius: 0.5,
		});

		// RIGHT HAND
		drawConnectors(this.canvasCtx, results.rightHandLandmarks, HAND_CONNECTIONS, {
			color: '#FFFFFF',
			lineWidth: 0.4,
		});
		drawLandmarks(this.canvasCtx, results.rightHandLandmarks, {
			color: '#FF0000',
			lineWidth: 0.4,
			radius: 0.5,
		});
		this.canvasCtx.restore();

		this.actualHolisticCoords = {
			pose: results.poseLandmarks ? results.poseLandmarks : null,
			face: results.faceLandmarks ? results.faceLandmarks.slice(0, 468) : null,
			leftHand: results.leftHandLandmarks ? results.leftHandLandmarks : null,
			rightHand: results.rightHandLandmarks ? results.rightHandLandmarks : null,
			segmentation: results.segmentationMask ? results.segmentationMask : null,
			ea: results.ea ? results.ea : null,
		};
	}

	public playAudio(signalName: any) {
		let utterance = new SpeechSynthesisUtterance(signalName);
		utterance.lang = 'es-ES';
		utterance.rate = 1;
		utterance.pitch = 1;
		utterance.volume = 1;
		speechSynthesis.speak(utterance);
	}

	public sendMessage() {
		if (this.actualHolisticCoords?.rightHand || this.actualHolisticCoords?.leftHand) {
			this.websocketService.socketConection(this.actualHolisticCoords);
		} else {
			this.signalPredicted = '';
		}
	}

	public setMessageInterval(boolCheck: boolean) {
		if (boolCheck) {
			this.messageInterval = 3000;
		} else {
			this.messageInterval = 1000;
		}
		clearInterval(this.captureInterval);
		this.captureInterval = setInterval(() => this.sendMessage(), this.messageInterval);
	}
}
