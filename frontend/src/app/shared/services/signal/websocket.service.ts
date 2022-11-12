import { Injectable } from '@angular/core';
import { webSocket, WebSocketSubject } from 'rxjs/webSocket';
import { environment } from 'src/environments/environment';

@Injectable({
	providedIn: 'root',
})
export class WebsocketService {
	constructor() {}

	private myWebSocket: WebSocketSubject<any> = webSocket(environment.wsURL + '/predict-signal');

	public socketConection(data: any): void {
		// Send a message to the server
		this.myWebSocket.next(data);
	}

	public getMessages(funct: any) {
		return this.myWebSocket.subscribe(
			// When messages are received by the server
			(msg) => funct(msg, this.myWebSocket),
			// When any error occurs§
			(err) => console.log(err),
			// When the connection is closed
			() => console.log('complete')
		);
	}
}
