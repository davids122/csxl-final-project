import { Component, ViewChild } from '@angular/core';
import { FormBuilder } from '@angular/forms';
import { EquipmentService } from '../equipment.service';
import { Router } from '@angular/router';
import {
  FormControl,
  FormGroupDirective,
  NgForm,
  Validators
} from '@angular/forms';
import { ErrorStateMatcher } from '@angular/material/core';
import { Profile } from 'src/app/models.module';
import { Subscription } from 'rxjs';
import { ProfileService } from 'src/app/profile/profile.service';

@Component({
  selector: 'app-equipment-waiver',
  templateUrl: './waiver.component.html',
  styleUrls: ['./waiver.component.css']
})
export class WaiverComponent {
  public static Route = {
    path: 'waiver',
    title: 'Sign Waiver',
    component: WaiverComponent
  };

  private profile: Profile | undefined;
  private profileSubscription!: Subscription;

  //Used to check to see if signature field is not empty
  formControl = new FormControl('', [Validators.required]);
  matcher = new ErrorStateMatcher();

  constructor(
    private equipmentService: EquipmentService,
    private profileSvc: ProfileService,
    public router: Router
  ) {
    this.profileSubscription = this.profileSvc.profile$.subscribe(
      (profile) => (this.profile = profile)
    );
  }

  // after agree to terms is clicked on waiver, update waiver field and route to equipment checkout component
  onSubmit() {
    var updated_profile = this.profile;
    updated_profile!.signed_equipment_wavier = true;

    this.equipmentService.update_waiver_field().subscribe({
      next: (value) => {
        this.router.navigateByUrl('equipment');
      },
      error: (err) => console.log(err)
    });
  }
}