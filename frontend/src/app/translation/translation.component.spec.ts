// @formatter:off
import 'zone.js';
import 'zone.js/testing';
// @formatter:on
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { TranslationComponent } from './translation.component';

describe('Pruebas Componente TranslationComponent', () => {
	beforeEach(async () => {
		await TestBed.configureTestingModule({
			imports: [RouterTestingModule, HttpClientTestingModule],
			declarations: [TranslationComponent],
		}).compileComponents();
	});
});
