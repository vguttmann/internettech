/*
last change: 24.06.2024
author: Vincent Guttmann

description: controls session properties
*/
import {Injectable} from '@angular/core';
import {ApiService} from "./api.service";
import {Message} from "./Message";
import {take} from "rxjs";

@Injectable({
    providedIn: 'root'
})
// service for session management
export class ControllerService {

    // creates the session manager
    constructor(private api: ApiService) {
    }

    // instance variables
    loggedIn: boolean = false;
    name!: string;
    sessionID!: number;
    messages: Message[] = [];

    // logs user in and assigns session id
    logIn(name: string) {
        this.name = name;
        this.loggedIn = true;
        this.api.get_sid().subscribe(result => this.sessionID = result as number);
        this.messages = [];

        // first contact message on every side open
        this.api.greeting().pipe(take(1)).subscribe(text =>
            this.api.get_time().pipe(take(1)).subscribe(time =>
                this.messages.push(new Message(text as string, "Bot", time as string))
            )
        )
    }
}
