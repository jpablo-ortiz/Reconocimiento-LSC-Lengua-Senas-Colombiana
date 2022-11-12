import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { ChartResultsComponent } from './chart-results/chart-results.component';
import { HomeComponent } from './home/home.component';
import { LoginComponent } from './login/login.component';
import { NewSignalComponent } from './new-signal/new-signal.component';
import { SignupComponent } from './signup/signup.component';
import { TrainingComponent } from './training/training.component';
import { TranslationComponent } from './translation/translation.component';

const routes: Routes = [
	{ path: 'home', component: HomeComponent },
	{ path: 'login', component: LoginComponent },
	{ path: 'signup', component: SignupComponent },
	{ path: 'new-signal', component: NewSignalComponent },
	{ path: 'training', component: TrainingComponent },
	{ path: 'translation', component: TranslationComponent },
	{ path: 'chart-results', component: ChartResultsComponent },
	{ path: '', redirectTo: '/home', pathMatch: 'full' },
	{ path: '**', redirectTo: '/home', pathMatch: 'full' }
];

@NgModule({
	imports: [RouterModule.forRoot(routes)],
	exports: [RouterModule],
})
export class AppRoutingModule {}
