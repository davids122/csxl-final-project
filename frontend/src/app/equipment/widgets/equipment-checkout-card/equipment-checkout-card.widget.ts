/**
 * The equipment checkout card widget is used to display all checkouts that are active
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
import { EquipmentCheckoutModel } from '../../equipment-checkout.model';

@Component({
  selector: 'equipment-checkout-card',
  templateUrl: './equipment-checkout-card.widget.html',
  styleUrls: ['./equipment-checkout-card.widget.css']
})
export class EquipmentCheckoutCard {
  @Input() checkouts!: Observable<EquipmentCheckoutModel[]>;
  @Output() returnEquipment = new EventEmitter<EquipmentCheckoutModel>();

  @ViewChild(MatTable) table: MatTable<any> | undefined;

  // Refresh the table on data update.
  public refreshTable() {
    if (this.table) {
      this.table.renderRows();
    }
  }

  columnsToDisplay = [
    'Name',
    'Model',
    'Equipment ID',
    'Return Due Date',
    'Action'
  ];
}
