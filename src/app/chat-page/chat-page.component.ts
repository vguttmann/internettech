/*
last change: 24.06.2024
author: Vincent Guttmann

description: logic of the chatbot component
*/
import { Component } from '@angular/core';
import { ControllerService } from "../controller.service";
import { NgIf } from "@angular/common";
import { ChatComponent } from "../chat/chat.component";
import { LoginFormComponent } from "../login-form/login-form.component";

@Component({
  selector: 'app-chatbot',
  standalone: true,
    imports: [
        NgIf,
        ChatComponent,
        LoginFormComponent
    ],
  templateUrl: './chat-page.component.html',
  styleUrl: './chat-page.component.css'
})
export class ChatPageComponent {
  // requires the session manager for display
  constructor(protected controller: ControllerService) {}
}
