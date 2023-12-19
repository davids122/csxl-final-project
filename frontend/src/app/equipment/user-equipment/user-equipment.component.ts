import { Component, OnInit } from '@angular/core';
import { EquipmentService } from '../equipment.service';
import { EquipmentType } from '../equipmentType.model';
import { Observable, Subscription, timer, tap } from 'rxjs';

@Component({
  selector: 'app-user-equipment',
  templateUrl: './user-equipment.component.html',
  styleUrls: ['./user-equipment.component.css']
})
export class UserEquipmentComponent implements OnInit {
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

  // Every 30 seconds update the equipment cards displayed to the user.
  ngOnInit(): void {
    timer(0, 30000)
      .pipe(
        tap(() => {
          this.updateEquipmentCards();
        })
      )
      .subscribe();
  }

  // Update the displayed equipment cards.
  updateEquipmentCards() {
    this.equipmentService
      .getAllEquipmentTypes()
      .subscribe((equipment) => (this.equipmentTypes$ = equipment));
  }
}
