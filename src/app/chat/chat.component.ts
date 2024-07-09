/*
last change: 24.06.2024
author: Vincent Guttmann

description: logic of the chat component
*/
import { Component, ElementRef, ViewChild } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import { NgForOf } from "@angular/common";
import { ApiService } from "../api.service";
import { ControllerService } from "../controller.service";
import { Message } from "../Message";
import { take } from "rxjs";

@Component({
    selector: 'app-chat',
    standalone: true,
    imports: [
        ReactiveFormsModule,
        FormsModule,
        NgForOf
    ],
    templateUrl: './chat.component.html',
    styleUrl: './chat.component.css'
})
// logic of the cat realised in the frontend
export class ChatComponent {
  // required for full scroll down
  @ViewChild('messageContainer') private messageContainer!: ElementRef<HTMLDivElement>;
  @ViewChild('chatInput') private chatInput!: ElementRef<HTMLInputElement>;

  // storage variables for the conversation
  message!: string;

  // requirement of api service and session controller
  constructor(private api: ApiService, protected controller: ControllerService) {}

  // function executed after each update on the screen
  ngAfterViewChecked() {
    this.scroll_down();
    this.chatInput.nativeElement.focus();
  }

  // scrolls message body completely down
  scroll_down() {
    try {
      this.messageContainer.nativeElement.scrollTop = this.messageContainer.nativeElement.scrollHeight;
    } catch (err) {}
  }

  // function which is executed when message is send
  sendMessage() {
    // if last message is from bot and own message has content
    if (this.message != "" && !(this.controller.messages[this.controller.messages.length - 1].author === this.controller.name)) {
      this.api.get_time().subscribe(time => {
        // actual transmission of the message to the chat
        this.pushMessage(this.message, this.controller.name, time as string, 100);
      });

      // initiate bot answer
      this.answerToMessage();
    }
  }

  // function that answers to the user
  answerToMessage() {
    this.api.get_time().pipe(take(1)).subscribe(time =>
      this.api.compute_input(this.controller.sessionID, this.message).pipe(take(1)).subscribe(response => {
        // clear user input field
        this.message = "";

        // transmits answer to display with fake "computing delay"
        this.pushMessage(response as string, "Bot", time as string, 800);
      })
    )
  }

  // method that adds message to display after delay
  async pushMessage(text: string, sender: string, time: string, wait: number) {
    await new Promise(_ => setTimeout(_, wait))

    this.controller.messages.push(new Message(text, sender, time))
  }
}
