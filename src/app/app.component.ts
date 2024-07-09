/*
last change: 24.06.2024
author: Tjorven Burdorf

description: logic of the main component
*/
import {Component} from '@angular/core';
import {RouterLink, RouterOutlet} from '@angular/router';

@Component({
    selector: 'app-root',
    standalone: true,
    imports: [RouterOutlet, RouterLink],
    templateUrl: './app.component.html',
    styleUrl: './app.component.css'
})
// logic of the main component
export class AppComponent {
    title = 'Projektarbeit - Tjorven Burdorf';
}
