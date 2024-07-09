/*
last change: 24.06.2024
author: Vincent Guttmann

description: represents a message with all of its properties
*/
/* represents a message with all of its properties */
export class Message {
    /* crates a message object */
    constructor(text: string, sender: string, time: string) {
        this.text = text;
        this.time = time;
        this.sender = sender;
        this.class = sender === "Bot" ? "bot" : "user";
    }

    /* instance variables */
    text: string; // represents text of the message
    sender: string; // represents the sender of the message
    time: string; // represents the time the message has been sent
    class: string; // represents the css class of the object
}
