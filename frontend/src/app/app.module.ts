import { HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { ChartResultsComponent } from './chart-results/chart-results.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { NewSignalComponent } from './new-signal/new-signal.component';
import { SignupComponent } from './signup/signup.component';
import { TrainingComponent } from './training/training.component';
import { TranslationComponent } from './translation/translation.component';

import { FusionChartsModule } from 'angular-fusioncharts';
import * as FusionCharts from 'fusioncharts';
import * as Charts from 'fusioncharts/fusioncharts.charts';
import * as FusionTheme from 'fusioncharts/themes/fusioncharts.theme.fusion';

FusionChartsModule.fcRoot(FusionCharts, Charts, FusionTheme);
@NgModule({
	declarations: [
		AppComponent,
		HomeComponent,
		NewSignalComponent,
		ChartResultsComponent,
		TrainingComponent,
		LoginComponent,
		SignupComponent,
		TranslationComponent,
	],
	imports: [AppRoutingModule, HttpClientModule, FormsModule, BrowserModule, FusionChartsModule, ReactiveFormsModule],
	providers: [],
	bootstrap: [AppComponent],
})
export class AppModule {}
