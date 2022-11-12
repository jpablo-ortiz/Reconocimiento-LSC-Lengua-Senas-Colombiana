import { Component } from '@angular/core';
import { AbstractControl, FormControl, FormGroup, Validators } from '@angular/forms';
import { Router } from '@angular/router';
import Swal from 'sweetalert2';
import { UserService } from '../shared/services/user/user.service';

@Component({
	selector: 'app-signup',
	templateUrl: './signup.component.html',
	styleUrls: ['./signup.component.css'],
})
export class SignupComponent {
	// --------------------- VARIABLES ---------------------

	roleA: string = '';
	roleC: string = '';

	formFields = new FormGroup({
		name: new FormControl('', [Validators.required, Validators.minLength(3)]),
		email: new FormControl('', [
			Validators.required,
			Validators.pattern('^[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,4}$'),
		]),
		password: new FormControl('', [Validators.required, Validators.minLength(6)]),
		role: new FormControl('', [Validators.required]),
	});

	// ----------------------- GETTERS -----------------------

	get Name(): AbstractControl {
		return this.formFields.get('name')!;
	}

	get Email(): AbstractControl {
		return this.formFields.get('email')!;
	}

	get Password(): AbstractControl {
		return this.formFields.get('password')!;
	}

	// --------------------- CONSTRUCTOR ---------------------

	constructor(private router: Router, private userService: UserService) {}

	// ---------------------- FUNCTIONS ----------------------

	public signup() {
		var name = this.formFields.value.name!;
		var email = this.formFields.value.email!;
		var password = this.formFields.value.password!;
		var rolUser: string = '';

		if (this.roleA !== '') {
			rolUser = this.roleA;
		} else if (this.roleC !== '') {
			rolUser = this.roleC;
		}
		this.userService.signup(name, email, password, rolUser).subscribe(
			(_res) => {
				this.successNotification();
				this.router.navigate(['/login']);
			},
			(err) => {
				if (err.status === 409) {
					this.errorUserAlreadyExistsNotification();
				} else {
					this.errorCreatingUserNotification();
				}
			}
		);
	}

	// ---------------------- NOTIFICATIONS ----------------------

	private successNotification() {
		Swal.fire({
			icon: 'success',
			title: 'Usuario creado',
			text: 'Usuario registrado correctamente',
		});
	}

	private errorUserAlreadyExistsNotification() {
		Swal.fire({
			icon: 'error',
			title: 'Error',
			text: 'Ya existe un usuario con el email ingresado',
		});
	}

	private errorCreatingUserNotification() {
		Swal.fire({
			icon: 'error',
			title: 'Error',
			text: 'Error al registrar usuario',
		});
	}
}
