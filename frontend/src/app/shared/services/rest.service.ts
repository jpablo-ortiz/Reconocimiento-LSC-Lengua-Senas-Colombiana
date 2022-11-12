import { HttpClient, HttpErrorResponse, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';
import Swal from 'sweetalert2';

@Injectable({
	providedIn: 'root',
})
export class RestService {
	constructor(private http: HttpClient) {}

	private signout(error: HttpErrorResponse): Observable<any> {
		// 401 Unauthorized- Signout actual user
		// Run this.signout() to clear localStorage and redirect to login page
		if (error.status === 401) {
			localStorage.clear();
			Swal.fire({
				icon: 'success',
				title: 'Sesión Cerrada',
				text: 'Gracias por usar nuestros servicios vuelve pronto!',
				showCloseButton: false,
				timer: 2000,
			});

			setTimeout(() => {
				localStorage.setItem('recargar', 'si');
				history.go(0);
			}, 2000);
		}
		return throwError(error);
	}

	public getHeaders() {
		let token = localStorage.getItem('token');
		return new HttpHeaders({
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`,
			Accept: 'application/json',
		});
	}

	public get<T>(url: string, httpHeader?: {}): Observable<T> {
		console.log('get', url);
		return this.http.get<T>(url, httpHeader).pipe(catchError(this.signout));
	}

	public post<T>(url: string, data: any, httpHeader?: {}): Observable<T> {
		console.log('post', url);
		return this.http.post<T>(url, data, httpHeader).pipe(catchError(this.signout));
	}

	public put<T>(url: string, data: any, httpHeader?: {}): Observable<T> {
		console.log('put', url);
		return this.http.put<T>(url, data, httpHeader).pipe(catchError(this.signout));
	}

	public delete<T>(url: string, httpHeader?: {}): Observable<T> {
		console.log('delete', url);
		return this.http.delete<T>(url, httpHeader).pipe(catchError(this.signout));
	}
}
