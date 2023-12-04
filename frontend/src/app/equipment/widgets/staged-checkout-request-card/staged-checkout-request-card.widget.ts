/**
 * The Equipment Card widget abstracts the implementation of each
 * individual equipment card from the whole equipment page.
 */

import {
  Component,
  EventEmitter,
  Input,
  Output,
  ViewChild
} from '@angular/core';
import { Router } from '@angular/router';
import { CheckoutRequestModel } from '../../checkoutRequest.model';
import { StagedCheckoutRequestModel } from '../../staged-checkout-request.model';
import { MatTable } from '@angular/material/table';
import { Observable } from 'rxjs';

@Component({
  selector: 'staged-checkout-request-card',
  templateUrl: './staged-checkout-request-card.widget.html',
  styleUrls: ['./staged-checkout-request-card.widget.css']
})
export class StageCard {
  @Input() stagedCheckoutRequests!: Observable<StagedCheckoutRequestModel[]>;
  @Output() approveStagedRequest =
    new EventEmitter<StagedCheckoutRequestModel>();
  @Output() cancelStagedRequest =
    new EventEmitter<StagedCheckoutRequestModel>();

  @ViewChild(MatTable) table: MatTable<any> | undefined;

  columnsToDisplay = ['Name', 'Model', 'Id', 'Action'];

  constructor(private router: Router) {}

  // Refresh the table on data update.
  public refreshTable() {
    if (this.table) {
      this.table.renderRows();
    }
  }

  // Set selected id for given staged request when the ambassador selects an id.
  idSelectionChange(id: Number, stagedRequest: StagedCheckoutRequestModel) {
    stagedRequest.selected_id = id;
  }
}
