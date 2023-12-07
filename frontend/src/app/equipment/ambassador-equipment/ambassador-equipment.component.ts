import { Component, OnInit, ViewChild } from '@angular/core';
import { Route, Router } from '@angular/router';
import { permissionGuard } from 'src/app/permission.guard';
import { profileResolver } from 'src/app/profile/profile.resolver';
import { EquipmentService } from '../equipment.service';
import { CheckoutRequestModel } from '../checkoutRequest.model';
import { Observable, map, reduce, tap, timer } from 'rxjs';
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
  /** Route information to be used in App Routing Module */
  public static Route: Route = {
    path: 'ambassador',
    component: AmbassadorEquipmentComponent,
    title: 'XL Equipment',
    canActivate: [permissionGuard('equipment.view.checkout', 'equipment')],
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
    this.setCheckoutRequestsLength();
    this.stagedCheckoutRequests$ = equipmentService.getAllStagedCheckouts();
    this.setStagedCheckoutLength();
    this.equipmentCheckouts$ = equipmentService.get_all_active_checkouts();
    this.setCheckoutsLength();
  }

  // Update checkoutRequestsTable every 5 seconds
  ngOnInit(): void {
    timer(0, 5000)
      .pipe(
        tap(() => {
          this.updateCheckoutRequestsTable();
        })
      )
      .subscribe();
  }

  // Updates the checkoutRequestTable
  updateCheckoutRequestsTable() {
    this.checkoutRequests$ = this.equipmentService.getAllRequest();
    this.setCheckoutRequestsLength();
    this.requestTable?.refreshTable();
  }

  // Updates the StagedCheckouts table
  updateStagedCheckoutTable() {
    this.stagedCheckoutRequests$ =
      this.equipmentService.getAllStagedCheckouts();
    this.setStagedCheckoutLength();
    this.stageTable?.refreshTable();
  }

  // Updates the activeCheckouts table
  updateCheckoutTable() {
    this.equipmentCheckouts$ = this.equipmentService.get_all_active_checkouts();
    this.setCheckoutsLength();
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

  // Calls deleteRequest service method to remove request from backend
  cancelRequest(request: CheckoutRequestModel) {
    this.equipmentService
      .deleteRequest(request)
      .subscribe(() => this.updateCheckoutRequestsTable());
  }

  // Approves a staged checkout calling service method; if successful, cancels the staged request and rerenders checkouts table
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

  // Cancels a staged request by deleting from database and rerendering staged requests table
  cancelStagedRequest(stagedRequest: StagedCheckoutRequestModel) {
    this.equipmentService.removeStagedCheckout(stagedRequest).subscribe({
      next: (value) => {
        this.updateStagedCheckoutTable();
      },
      error: (err) => console.log(err)
    });
  }

  // Gets the length of the observable array of checkout request models.
  setCheckoutRequestsLength() {
    this.checkoutRequests$.subscribe((array) => {
      this.checkoutRequestsLength = array.length;
    });
  }

  // Gets the length of the observable array of staged checkout request models
  setStagedCheckoutLength() {
    this.stagedCheckoutRequests$.subscribe((array) => {
      this.stagedCheckoutRequestsLength = array.length;
    });
  }
  // Gets the length of the observable array of checkout models
  setCheckoutsLength() {
    this.equipmentCheckouts$.subscribe((array) => {
      this.checkoutsLength = array.length;
    });
  }

  // Returns a piece of equipment by calling service method and rerendering if successful
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
