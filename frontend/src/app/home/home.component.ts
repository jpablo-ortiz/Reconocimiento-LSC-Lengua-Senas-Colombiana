import { Component, OnInit } from '@angular/core';
import { gsap } from 'gsap';
import { Draggable } from 'gsap/Draggable';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

@Component({
	selector: 'app-home',
	templateUrl: './home.component.html',
	styleUrls: ['./home.component.css'],
})
export class HomeComponent implements OnInit {
	// --------------------- VARIABLES ---------------------

	team = [
		{
			profile: '../assets/images/juan.jpg',
			names: 'Juan Pablo',
			lastnames: 'Ortiz Rubio',
			email: 'jpablo.ortiz@javeriana.edu.co',
			linkedin: 'https://www.linkedin.com/in/juan-pablo-ortiz-rubio/',
			github: 'https://github.com/jpablo-ortiz',
		},
		{
			profile: '../assets/images/kenneth.jpg',
			names: 'Kenneth David',
			apellido: 'Leonel Triana',
			email: 'kdavidleonelt@javeriana.edu.co',
			linkedin: 'www.linkedin.com/in/kenneth-david-leonel-triana-4920b5162',
			github: 'https://github.com/kennethLeonel',
		},
		{
			profile: '../assets/images/camilo.jpeg',
			names: 'Camilo Andrés',
			apellido: 'Sandoval Guayambuco',
			email: 'sandovalg.camilo@javeriana.edu.co',
			linkedin: 'https://www.linkedin.com/in/camilo-andres-sandoval-guayambuco/',
			github: 'https://github.com/camilosan10',
		},
		{
			profile: '../assets/images/cristian.jpg',
			names: 'Cristian Javier',
			apellido: 'Da camara Sousa',
			email: 'cristianj.dacamaras@javeriana.edu.co',
			linkedin: 'https://www.linkedin.com/in/cristian-da-camara-844a0a129/',
			github: 'https://github.com/CristianJavierDaCamaraSousa',
		},
	];

	// --------------------- CONSTRUCTOR ---------------------

	constructor() {}

	// ------------------- NgOn FUNCTIONS --------------------

	ngOnInit(): void {
		gsap.registerPlugin(ScrollTrigger, Draggable);
		// Init ScrollTrigger
		document.querySelectorAll('.box').forEach((box) => {
			const scrollBox = gsap.timeline({
				scrollTrigger: {
					trigger: box,
					pin: false,
					start: 'top center',
					end: 'center center',
					markers: false,
					toggleActions: 'play none none reverse',
				},
			});
			scrollBox.from(box, { y: 40, opacity: 0 });
		});
	}
}
