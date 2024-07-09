/*
last change: 24.06.2024
author: Vincent Guttmann

description: logic of the evaluation component
*/
import {Component} from '@angular/core';
import {ApiService} from "../api.service";
import {ControllerService} from "../controller.service";
import {NgForOf, NgIf, NgOptimizedImage} from "@angular/common";
import {ChatComponent} from "../chat/chat.component";
import {ChatbotComponent} from "../chatbot/chatbot.component";
import {RouterLink} from "@angular/router";

@Component({
    selector: 'app-evaluation',
    standalone: true,
    imports: [
        NgForOf,
        NgIf,
        ChatComponent,
        ChatbotComponent,
        NgOptimizedImage,
        RouterLink
    ],
    templateUrl: './evaluation.component.html',
    styleUrl: './evaluation.component.css'
})
// logic of the component that provides the complete evaluation
export class EvaluationComponent {
    // api service and session controller are required
    constructor(private api: ApiService, private controller: ControllerService) {
    }

    // instance variables representing the own name and the evaluation
    evaluation_data: any[][] = []
    name?: string

    // function, that executes on page initialisation
    ngOnInit() {
        this.api.get_evaluation(this.controller.sessionID).subscribe(data => this.evaluation_data = data as any)
        this.name = this.controller.name
    }
}
