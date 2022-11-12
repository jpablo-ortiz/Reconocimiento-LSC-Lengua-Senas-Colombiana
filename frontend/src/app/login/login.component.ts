import { Component, OnInit } from '@angular/core';
import { AbstractControl, FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import Swal from 'sweetalert2';
import { UserService } from '../shared/services/user/user.service';

@Component({
	selector: 'app-login',
	templateUrl: './login.component.html',
	styleUrls: ['./login.component.css'],
})
export class LoginComponent implements OnInit {
	// --------------------- VARIABLES ---------------------

	token: any;
	formFields = new FormGroup({
		email: new FormControl('', [
			Validators.required,
			Validators.pattern('^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$'),
		]),
		password: new FormControl('', [Validators.required, Validators.minLength(6)]),
	});

	// ----------------------- GETTERS -----------------------

	get Email(): AbstractControl {
		return this.formFields.get('email')!;
	}

	get Password(): AbstractControl {
		return this.formFields.get('password')!;
	}

	// --------------------- CONSTRUCTOR ---------------------

	constructor(private router: Router, private userService: UserService) {}

	// ---------------------- FUNCTIONS ----------------------

	ngOnInit(): void {
		if (localStorage.getItem('recargar') == 'si') {
			this.router.navigate(['/home']);
		}
	}

	public login() {
		var email = this.formFields.value.email!;
		var password = this.formFields.value.password!;
		this.userService.login(email, password).subscribe(
			(res) => {
				this.token = res.access_token;
				localStorage.setItem('token', res.access_token);

				localStorage.setItem('role', res.role);
				localStorage.setItem('usuario', res.name);

				localStorage.setItem('recargar', 'si');
				this.successNotification();
				history.go(0);
			},
			(_error) => {
				this.errorNotification();
			}
		);
	}

	// ---------------------- NOTIFICATIONS ----------------------

	private successNotification() {
		Swal.fire({
			icon: 'success',
			title: 'Bienvenido ' + localStorage.getItem('usuario'),
		});
	}

	private errorNotification() {
		Swal.fire({
			icon: 'error',
			title: 'Error',
			text: 'Usuario o contraseña incorrectos',
		});
	}
}
