import { Component } from '@angular/core';
import { EquipmentService } from '../equipment.service';
import { EquipmentType } from '../equipmentType.model';
import { Observable, Subscription } from 'rxjs';

@Component({
  selector: 'app-user-equipment',
  templateUrl: './user-equipment.component.html',
  styleUrls: ['./user-equipment.component.css']
})
export class UserEquipmentComponent {
  /** Route information to be used in App Routing Module */
  public static Route = {
    path: '',
    title: 'User Equipment Checkout',
    component: UserEquipmentComponent
  };

  public equipmentTypes$: EquipmentType[] | undefined;

  constructor(public equipmentService: EquipmentService) {
    equipmentService
      .getAllEquipmentTypes()
      .subscribe((equipment) => (this.equipmentTypes$ = equipment));
  }
}
