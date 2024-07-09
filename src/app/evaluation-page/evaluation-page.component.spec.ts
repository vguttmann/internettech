import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EvaluationPageComponent } from './evaluation-page.component';

// file from angular
describe('EvaluationComponent', () => {
  let component: EvaluationPageComponent;
  let fixture: ComponentFixture<EvaluationPageComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [EvaluationPageComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(EvaluationPageComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
