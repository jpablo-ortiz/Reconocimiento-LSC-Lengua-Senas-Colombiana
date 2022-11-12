import { AfterViewInit, Component, ElementRef, ViewChild } from '@angular/core';
import { AbstractControl, FormControl, FormGroup, Validators } from '@angular/forms';
import Swal from 'sweetalert2';
import { SignalService } from '../shared/services/signal/signal.service';

@Component({
	selector: 'app-new-signal',
	templateUrl: './new-signal.component.html',
	styleUrls: ['./new-signal.component.css'],
})
export class NewSignalComponent implements AfterViewInit {
	// --------------------- VARIABLES ---------------------

	inputText: string = '';
	inputElement: any;

	isCaptured!: boolean;
	captures: string[] = [];
	processedPhotos: string[] = [];

	WIDTH = 640;
	HEIGHT = 480;
	error: any;

	@ViewChild('video')
	public video!: ElementRef;

	@ViewChild('canvas')
	public canvas!: ElementRef;

	formFields = new FormGroup({
		name: new FormControl('', [Validators.required]),
	});

	get Name(): AbstractControl {
		return this.formFields.get('name')!;
	}

	// --------------------- CONSTRUCTOR ---------------------

	constructor(private signalService: SignalService) {}

	// ------------------- NgOn FUNCTIONS --------------------

	ngOnInit(): void {
		this.inputElement = document.getElementById('nombreSena');
	}

	async ngAfterViewInit() {
		await this.setupDevices();
	}

	// ---------------------- FUNCTIONS ----------------------

	public async setupDevices() {
		if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
			try {
				const stream = await navigator.mediaDevices.getUserMedia({
					video: {
						height: this.HEIGHT,
						width: this.WIDTH,
					},
				});
				if (stream) {
					this.video.nativeElement.srcObject = stream;
					this.video.nativeElement.play();
					this.error = null;
				} else {
					this.error = 'No tienes dispositivo de camara';
				}
			} catch (e) {
				this.error = e;
			}
		}
	}

	public capture() {
		this.drawImageToCanvas(this.video.nativeElement);
		this.captures.push(this.canvas.nativeElement.toDataURL('image/png'));
		this.isCaptured = false;
	}

	public removeCurrent() {
		this.isCaptured = false;
	}

	public setPhoto(idx: number) {
		this.isCaptured = true;
		var image = new Image();
		image.src = this.captures[idx];
		this.drawImageToCanvas(image);
	}

	public drawImageToCanvas(image: any) {
		this.canvas.nativeElement.getContext('2d').drawImage(image, 0, 0, this.WIDTH, this.HEIGHT);
	}

	public deletePhoto(idx: number) {
		this.captures = this.captures.filter((item) => item !== this.captures[idx]);
		this.isCaptured = false;
	}

	public deleteAll() {
		this.captures = [];
		this.isCaptured = false;
	}

	public getBase64StringFromDataURL(captures: string[]) {
		for (let i = 0; i < captures.length; i++) {
			this.processedPhotos.push(captures[i].replace('data:', '').replace(/^.+,/, ''));
		}
	}

	public process() {
		this.inputText = this.formFields.value.name!;
		if (this.captures.length <= 0) {
			this.notPhotosToProcessNotification();
		} else if (this.inputText == '') {
			this.nameOfSignalNotSpecifiedNotification();
		} else if (this.captures.length < 10) {
			this.minimumPhotosToProcessNotification();
		} else {
			this.getBase64StringFromDataURL(this.captures);
			this.signalService.createSignal(this.processedPhotos, this.inputText).subscribe(
				(_res) => {
					this.succesSignalCreationNotification();
					this.captures = [];
					this.isCaptured = false;
					this.inputText = '';
					this.formFields.reset();
					this.processedPhotos = [];
				},
				(_error) => {
					this.errorSignalCreationNotification();
				}
			);
		}
	}

	// ---------------------- NOTIFICATIONS ----------------------

	private notPhotosToProcessNotification() {
		Swal.fire({
			icon: 'error',
			title: 'Oops...',
			text: 'No hay fotos para procesar!',
			confirmButtonText: 'Aceptar',
		});
	}

	private nameOfSignalNotSpecifiedNotification() {
		Swal.fire({
			icon: 'error',
			title: 'Oops...',
			text: 'No se ha especificado el nombre de la seña a procesar!',
			confirmButtonText: 'Aceptar',
		});
	}

	private minimumPhotosToProcessNotification() {
		Swal.fire({
			icon: 'error',
			title: 'Oops...',
			text: 'Se necesitan al menos 10 fotos para procesar!',
			confirmButtonText: 'Aceptar',
		});
	}

	private succesSignalCreationNotification() {
		Swal.fire({
			icon: 'success',
			title: 'Genial',
			text: 'Se ha subido la seña correctamente',
			confirmButtonText: 'Aceptar',
		});
	}

	private errorSignalCreationNotification() {
		Swal.fire({
			icon: 'error',
			title: 'No se puede procesar realizar esta acción',
			text: 'Porfavor verificar que el usuario tenga los permisos necesarios.',
		});
	}
}
