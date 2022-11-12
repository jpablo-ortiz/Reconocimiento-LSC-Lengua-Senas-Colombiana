import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import Swal from 'sweetalert2';

@Component({
	selector: 'app-root',
	templateUrl: './app.component.html',
	styleUrls: ['./app.component.css'],
})
export class AppComponent implements OnInit {
	// --------------------- VARIABLES ---------------------

	title = 'Reconocimiento LSC';
	username = localStorage.getItem('usuario') || '';
	isLogged = false;

	// --------------------- CONSTRUCTOR ---------------------

	constructor(public router: Router) {}

	// ------------------- NgOn FUNCTIONS --------------------

	ngOnInit() {
		if (
			localStorage.getItem('token') ||
			localStorage.getItem('token') != null ||
			localStorage.getItem('token') == ''
		) {
			this.isLogged = true;
		}
		if (localStorage.getItem('recargar') == 'si') {
			localStorage.removeItem('recargar');
			this.goTo('/home');
		}
	}

	// ---------------------- FUNCTIONS ----------------------

	public signout() {
		localStorage.clear();
		this.signOutNotification();
		setTimeout(() => {
			localStorage.setItem('recargar', 'si');
			history.go(0);
		}, 2000);
	}

	public goTo(path: string) {
		this.router.navigate([path]);
	}

	// ---------------------- NOTIFICATIONS ----------------------

	private signOutNotification() {
		Swal.fire({
			icon: 'success',
			title: 'Sesión Cerrada',
			text: 'Gracias por usar nuestros servicios vuelve pronto!',
			showCloseButton: false,
			timer: 2000,
		});
	}
}
