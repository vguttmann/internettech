/*
last change: 24.06.2024
author: Vincent Guttmann

description: represents a message with all of its properties
*/

/** Represents a message with all of its properties */
export class Message {
  /** Represents the text content of the message. */
  text: string;
  /** Represents the author of the message. */
  author: string;
  /** Represents the time the message has been sent. */
  time: string;
  /** Represents the css class of the object. */
  cssClass: string;

  /** Crate a message object */
  constructor(text: string, author: string, time: string) {
    this.text = text;
    this.time = time;
    this.author = author;
    this.cssClass = author === "Bot" ? "bot" : "user";
  }
}
