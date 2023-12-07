import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { EquipmentService } from '../equipment.service';
import { Observable, tap, timer, pipe, Subscription } from 'rxjs';
import { CheckoutRequestModel } from '../checkoutRequest.model';

@Component({
  selector: 'app-equipment-checkout-confirmation',
  templateUrl: './equipment-checkout-confirmation.component.html',
  styleUrls: ['./equipment-checkout-confirmation.component.css']
})
export class EquipmentCheckoutConfirmationComponent {
  /** Route information to be used in App Routing Module */
  public static Route = {
    path: 'checkout',
    title: 'Checkout Confirmation',
    component: EquipmentCheckoutConfirmationComponent
  };

  constructor(private router: Router) {}
}
