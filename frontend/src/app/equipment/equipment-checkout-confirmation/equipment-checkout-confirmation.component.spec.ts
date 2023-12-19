import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EquipmentCheckoutConfirmationComponent } from './equipment-checkout-confirmation.component';

describe('EquipmentCheckoutConfirmationComponent', () => {
  let component: EquipmentCheckoutConfirmationComponent;
  let fixture: ComponentFixture<EquipmentCheckoutConfirmationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EquipmentCheckoutConfirmationComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(EquipmentCheckoutConfirmationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
