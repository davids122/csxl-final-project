/**
 * The Equipment Card widget abstracts the implementation of each
 * individual equipment card from the whole equipment page.
 */

import { Component, Input } from '@angular/core';
import { EquipmentType } from '../../equipmentType.model';
import { Router } from '@angular/router';
import { EquipmentService } from '../../equipment.service';
import { Profile } from 'src/app/models.module';
import { Subscription } from 'rxjs';
import { ProfileService } from 'src/app/profile/profile.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { HttpErrorResponse } from '@angular/common/http';

@Component({
  selector: 'equipment-card',
  templateUrl: './equipment-card.widget.html',
  styleUrls: ['./equipment-card.widget.css']
})
export class EquipmentCard {
  /** Inputs and outputs go here */

  private profile: Profile | undefined;
  private profileSubscription!: Subscription;

  @Input() equipmentType!: EquipmentType;

  constructor(
    public router: Router,
    public equipmentService: EquipmentService,
    protected profileSvc: ProfileService,
    protected snackBar: MatSnackBar
  ) {
    this.profileSubscription = this.profileSvc.profile$.subscribe(
      (profile) => (this.profile = profile)
    );
  }

  onCheckout() {
    if (this.profile === undefined) {
      throw new Error('Only allowed for logged in users.');
    }
    if (!this.profile.signed_equipment_wavier) {
      this.router.navigateByUrl('/equipment/waiver');
    } else {
      this.equipmentService.addRequest(this.equipmentType).subscribe({
        next: (checkoutRequest) => {
          console.log('success!');
          this.router.navigateByUrl('/equipment/checkout');
        },
        error: (error) => {
          if (error instanceof HttpErrorResponse) {
            this.onError(error);
          } else {
            console.log(error);
          }
        }
      });
    }
  }

  onError(err: HttpErrorResponse) {
    this.snackBar.open(err.error.detail, '', { duration: 4000 });
  }
}
