/*
last change: 24.06.2024
author: Tjorven Burdorf

description: logic of the data component
*/
import {Component} from '@angular/core';
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {RouterLink} from "@angular/router";
import {ControllerService} from "../controller.service";

@Component({
    selector: 'app-data',
    standalone: true,
    imports: [
        ReactiveFormsModule,
        RouterLink,
        FormsModule
    ],
    templateUrl: './data.component.html',
    styleUrl: './data.component.css'
})
export class DataComponent {
    // login requires the session controller
    constructor(protected controller: ControllerService) {
    }

    // main functionality is to get the username
    username: string = "";

    // button logic to commit the username
    confirm() {
        if (this.username != "") {
            this.controller.logIn(this.username)
        }
    }
}
