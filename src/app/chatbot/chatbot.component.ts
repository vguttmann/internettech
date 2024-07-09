/*
last change: 24.06.2024
author: Tjorven Burdorf

description: logic of the chatbot component
*/
import { Component } from '@angular/core';
import { ControllerService } from "../controller.service";
import {NgIf} from "@angular/common";
import {ChatComponent} from "../chat/chat.component";
import {LoginComponent} from "../login/login.component";
import {DataComponent} from "../data/data.component";

@Component({
  selector: 'app-chatbot',
  standalone: true,
    imports: [
        NgIf,
        ChatComponent,
        LoginComponent,
        DataComponent
    ],
  templateUrl: './chatbot.component.html',
  styleUrl: './chatbot.component.css'
})
export class ChatbotComponent {
    // requires the session manager for display
    constructor(protected controller: ControllerService) {
    }
}
