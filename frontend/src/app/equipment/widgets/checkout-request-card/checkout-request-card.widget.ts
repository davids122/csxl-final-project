/**
 * The checkout request card widget is used to display all checkout requests that have not yet
 * been accepted by an ambassador.
 */
import {
  Component,
  EventEmitter,
  Input,
  Output,
  ViewChild
} from '@angular/core';
import { CheckoutRequestModel } from '../../checkoutRequest.model';
import { Observable } from 'rxjs';
import { MatTable } from '@angular/material/table';

@Component({
  selector: 'checkout-request-card',
  templateUrl: './checkout-request-card.widget.html',
  styleUrls: ['./checkout-request-card.widget.css']
})
export class CheckoutRequestCard {
  @Input() checkoutRequests!: Observable<CheckoutRequestModel[]>;
  @Output() approveRequest = new EventEmitter<CheckoutRequestModel>();
  @Output() cancelRequest = new EventEmitter<CheckoutRequestModel>();

  @ViewChild(MatTable) table: MatTable<any> | undefined;

  // Refresh the table on data update.
  public refreshTable() {
    if (this.table) {
      this.table.renderRows();
    }
  }

  columnsToDisplay = ['Name', 'Model', 'Action'];
}
