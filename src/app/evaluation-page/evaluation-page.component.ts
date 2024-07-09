/*
last change: 24.06.2024
author: Vincent Guttmann

description: logic of the evaluation component
*/

import { Component } from '@angular/core';
import { ApiService } from "../api.service";
import { ControllerService } from "../controller.service";
import { NgForOf, NgIf, NgOptimizedImage } from "@angular/common";
import { ChatComponent } from "../chat/chat.component";
import { ChatPageComponent } from "../chat-page/chat-page.component";
import { RouterLink } from "@angular/router";

@Component({
  selector: 'app-evaluation',
  standalone: true,
  imports: [
    NgForOf,
    NgIf,
    ChatComponent,
    ChatPageComponent,
    NgOptimizedImage,
    RouterLink
  ],
  templateUrl: './evaluation-page.component.html',
  styleUrl: './evaluation-page.component.css'
})
// logic of the component that provides the complete evaluation
export class EvaluationPageComponent {
  evaluationData: any[] = []
  name?: string

  // api service and session controller are required
  constructor(private api: ApiService, private controller: ControllerService) {}

  // function, that executes on page initialisation
  ngOnInit() {
    this.api.get_evaluation(this.controller.sessionID).subscribe(data => this.evaluationData = JSON.parse(data as any) as any[])
    this.name = this.controller.name
  }
}
