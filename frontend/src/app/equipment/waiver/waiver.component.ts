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
import { MatSnackBar } from '@angular/material/snack-bar';

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

  //Used to check to see if signature field is not empty
  formControl = new FormControl('', [Validators.required]);
  matcher = new ErrorStateMatcher();

  constructor(
    private equipmentService: EquipmentService,
    private profileSvc: ProfileService,
    public router: Router,
    protected snackBar: MatSnackBar
  ) {
    this.profileSvc.profile$.subscribe((profile) => (this.profile = profile));
  }

  // after agree to terms is clicked on waiver, update waiver field and route to equipment checkout component
  onSubmit() {
    var updated_profile = this.profile;
    updated_profile!.signed_equipment_wavier = true;

    this.equipmentService.update_waiver_field().subscribe({
      next: (value) => {
        this.router.navigateByUrl('equipment').then((navigated: boolean) => {
          if (navigated) {
            this.snackBar.open('You may now checkout equipment!', '', {
              duration: 4000
            });
          }
        });
      },
      error: (err) => console.log(err)
    });
  }
}
