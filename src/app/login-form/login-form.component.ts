/*
last change: 24.06.2024
author: Vincent Guttmann

description: logic of the data component
*/

import { Component } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import { RouterLink } from "@angular/router";
import { ControllerService } from "../controller.service";

@Component({
  selector: 'app-data',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    RouterLink,
    FormsModule
  ],
  templateUrl: './login-form.component.html',
  styleUrl: './login-form.component.css'
})
export class LoginFormComponent {
  username: string = "";

  // login requires the session controller
  constructor(protected controller: ControllerService) {}

  // logs in if the username is not empty
  begin() {
    if (this.username) this.controller.logIn(this.username);
  }
}
