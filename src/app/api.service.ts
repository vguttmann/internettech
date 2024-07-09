/*
last change: 24.06.2024
author: Vincent Guttmann

description: controls all api applications
*/

import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { take } from "rxjs";

// adjust ip with the one of the server
const BASE_URL = 'http://bugfishing.duckdns.org:8000';

@Injectable({
    providedIn: 'root'
})
// represents a service executing api calls which is in the whole app available
export class ApiService {
  // calls are executed with the httpClient as single subscriptions
  constructor(private http: HttpClient) {}

  greeting() { return this.http.get(`${BASE_URL}/`).pipe(take(1)); }

  get_sid() { return this.http.get(`${BASE_URL}/sid`).pipe(take(1)); }

  get_time() { return this.http.get(`${BASE_URL}/time`).pipe(take(1)); }

  compute_input(sid: number, text: string) { return this.http.get(`${BASE_URL}/compute/${sid}/${text}`).pipe(take(1)); }

  get_evaluation(sid: number) { return this.http.get(`${BASE_URL}/evaluation/${sid}`).pipe(take(1)); }
}
