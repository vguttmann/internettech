/*
last change: 24.06.2024
author: Vincent Guttmann

description: router for the entire application
*/

import { Routes } from '@angular/router';
import { ChatPageComponent } from "./chat-page/chat-page.component";
import { AboutComponent } from "./about/about.component";
import { ImprintComponent } from "./imprint/imprint.component";
import { ExternalComponent } from "./external/external.component";
import { EvaluationPageComponent } from "./evaluation-page/evaluation-page.component";

// represents the routes and the corresponding paths and components
export const routes: Routes = [
  {path: '', redirectTo: 'chat', pathMatch: 'full'},
  {path: 'chat', component: ChatPageComponent},
  {path: 'evaluation', component: EvaluationPageComponent},
  {path: 'about', component: AboutComponent},
  {path: 'imprint', component: ImprintComponent},
  {path: 'external', component: ExternalComponent}
];
