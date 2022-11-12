import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';
import { RestService } from '../rest.service';

@Injectable({
	providedIn: 'root',
})
export class UserService {
	constructor(private restService: RestService) {}

	public signup(name: string, email: string, password: string, role: string): Observable<any> {
		const url = environment.baseURL + '/signup';
		return this.restService.post<any>(
			url,
			{
				name: name,
				username: email,
				password: password,
				role: role,
			},
			{
				Accept: 'application/json',
				'Content-Type': 'application/json',
			}
		);
	}

	public login(email: string, password: string): Observable<any> {
		const url = environment.baseURL + '/login';
		return this.restService.post<any>(
			url,
			{
				username: email,
				password: password,
			},
			{ Accept: 'application/json', 'Content-Type': 'application/json' }
		);
	}
}
