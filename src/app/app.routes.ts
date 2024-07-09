/*
last change: 24.06.2024
author: Vincent Guttmann

description: router for the entire application
*/
import {Routes} from '@angular/router';
import {LoginComponent} from "./login/login.component";
import {ChatbotComponent} from "./chatbot/chatbot.component";
import {AboutComponent} from "./about/about.component";
import {ImprintComponent} from "./imprint/imprint.component";
import {ExternalComponent} from "./external/external.component";
import {EvaluationComponent} from "./evaluation/evaluation.component";

// represents the routes and the corresponding paths and components
export const routes: Routes = [
    {path: '', redirectTo: 'login', pathMatch: 'full'},
    {path: 'login', component: LoginComponent},
    {path: 'chat', component: ChatbotComponent},
    {path: 'evaluation', component: EvaluationComponent},
    {path: 'about', component: AboutComponent},
    {path: 'imprint', component: ImprintComponent},
    {path: 'external', component: ExternalComponent}
];
