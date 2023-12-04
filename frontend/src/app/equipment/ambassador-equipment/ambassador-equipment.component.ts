import { Component, OnInit, ViewChild } from '@angular/core';
import { Route, Router } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { EquipmentService } from '../equipment.service';
import { CheckoutRequestModel } from '../checkoutRequest.model';
import { Observable, reduce, tap, timer } from 'rxjs';
import { StagedCheckoutRequestModel } from '../staged-checkout-request.model';
import { StageCard } from '../widgets/staged-checkout-request-card/staged-checkout-request-card.widget';
import { CheckoutRequestCard } from '../widgets/checkout-request-card/checkout-request-card.widget';
import { EquipmentCheckoutCard } from '../widgets/equipment-checkout-card/equipment-checkout-card.widget';
import { EquipmentCheckoutConfirmationComponent } from '../equipment-checkout-confirmation/equipment-checkout-confirmation.component';
import { EquipmentCheckoutModel } from '../equipment-checkout.model';

@Component({
  selector: 'app-ambassador-equipment',
  templateUrl: './ambassador-equipment.component.html',
  styleUrls: ['./ambassador-equipment.component.css']
})
export class AmbassadorEquipmentComponent implements OnInit {
  public static Route: Route = {
    path: 'ambassador',
    component: AmbassadorEquipmentComponent,
    title: 'XL Equipment',
    canActivate: [permissionGuard('equipment.update', 'equipment')],
    resolve: { profile: profileResolver }
  };

  checkoutRequests$: Observable<CheckoutRequestModel[]>;
  checkoutRequestsLength: number = 0;
  stagedCheckoutRequests$: Observable<StagedCheckoutRequestModel[]>;
  stagedCheckoutRequestsLength: number = 0;
  equipmentCheckouts$: Observable<EquipmentCheckoutModel[]>;
  checkoutsLength: number = 0;

  @ViewChild(StageCard) stageTable: StageCard | undefined;
  @ViewChild(CheckoutRequestCard) requestTable: CheckoutRequestCard | undefined;
  @ViewChild(EquipmentCheckoutCard) checkoutTable:
    | EquipmentCheckoutCard
    | undefined;

  constructor(
    public router: Router,
    private equipmentService: EquipmentService
  ) {
    this.checkoutRequests$ = equipmentService.getAllRequest();
    this.getCheckoutRequestLength();
    this.stagedCheckoutRequests$ = equipmentService.getAllStagedCheckouts();
    this.getStagedCheckoutLength();
    this.equipmentCheckouts$ = equipmentService.get_all_active_checkouts();
    this.getCheckoutsLength();
    this.stagedCheckoutRequests$.subscribe({
      next: (value) => {
        console.log(value);
      },
      error: (error) => {
        console.log(error);
      }
    });
  }

  // every 5 seconds call the get all request service method to update ambassador equipment checkout page.
  ngOnInit(): void {
    timer(0, 5000)
      .pipe(
        tap(() => {
          this.updateCheckoutRequestsTable();
        })
      )
      .subscribe();
  }

  updateCheckoutRequestsTable() {
    //updates the checkout request table
    this.checkoutRequests$ = this.equipmentService.getAllRequest();
    this.getCheckoutRequestLength();
    this.requestTable?.refreshTable();
  }

  updateStagedCheckoutTable() {
    //updates the staged checkout request table
    this.stagedCheckoutRequests$ =
      this.equipmentService.getAllStagedCheckouts();
    this.getStagedCheckoutLength();
    this.stageTable?.refreshTable();
  }

  updateCheckoutTable() {
    //updates the checkout table
    this.equipmentCheckouts$ = this.equipmentService.get_all_active_checkouts();
    this.getCheckoutsLength();
    this.checkoutTable?.refreshTable();
  }

  // TODO: move logic into service
  approveRequest(request: CheckoutRequestModel) {
    // Convert request into staged request.
    let id_choices: Number[] = [];
    let equipment_list = this.equipmentService.getAllEquipmentByModel(
      request.model
    );
    equipment_list.subscribe({
      next(equipment_arr) {
        equipment_arr.forEach((item) => {
          id_choices?.push(item.equipment_id);
        });
      }
    });
    let user_name = request.user_name;
    let model = request.model;
    let selected_id = undefined;
    let pid = request.pid;
    let stagedRequest: StagedCheckoutRequestModel = {
      user_name: user_name,
      model: model,
      id_choices: id_choices,
      selected_id: null,
      pid: pid
    };
    this.equipmentService.approveRequest(stagedRequest).subscribe({
      next: () => {
        this.cancelRequest(request);
        this.updateStagedCheckoutTable();
        this.updateCheckoutRequestsTable();
      },
      error: (error) => {
        console.log(error);
      }
    });
  }

  cancelRequest(request: CheckoutRequestModel) {
    // Calls the proper API route to remove a request from checkout requests table in the backend.
    this.equipmentService
      .deleteRequest(request)
      .subscribe(() => this.updateCheckoutRequestsTable());
  }

  approveStagedRequest(request: StagedCheckoutRequestModel) {
    // Calls the proper API route to move request into checkouts table in backend.
    this.equipmentService.create_checkout(request).subscribe({
      next: (value) => {
        this.cancelStagedRequest(request);
        this.updateCheckoutTable();
      },
      error: (err) => console.log(err)
    });
  }

  cancelStagedRequest(stagedRequest: StagedCheckoutRequestModel) {
    this.equipmentService.removeStagedCheckout(stagedRequest).subscribe({
      next: (value) => {
        this.updateStagedCheckoutTable();
      },
      error: (err) => console.log(err)
    });
  }

  // Gets the length of the observable array of checkout request models.
  getCheckoutRequestLength() {
    this.checkoutRequests$
      .pipe(
        reduce((count) => count + 1, 1) // Starts with 0 and increments by 1 for each item
      )
      .subscribe((count) => (this.checkoutRequestsLength = count));
  }

  getStagedCheckoutLength() {
    this.stagedCheckoutRequests$
      .pipe(
        reduce((count) => count + 1, 1) // Starts with 0 and increments by 1 for each item
      )
      .subscribe((count) => (this.stagedCheckoutRequestsLength = count));
  }

  getCheckoutsLength() {
    this.equipmentCheckouts$
      .pipe(
        reduce((count) => count + 1, 1) // Starts with 0 and increments by 1 for each item
      )
      .subscribe((count) => (this.checkoutsLength = count));
  }

  returnEquipment(checkout: EquipmentCheckoutModel) {
    // Calls proper API route to return an equipment checkout
    this.equipmentService.returnCheckout(checkout).subscribe({
      next: (value) => {
        this.updateCheckoutTable();
      },
      error: (err) => console.log(err)
    });
  }
}
