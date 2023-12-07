import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { UserEquipmentComponent } from './user-equipment/user-equipment.component';
import { WaiverComponent } from './waiver/waiver.component';
import { EquipmentCheckoutConfirmationComponent } from './equipment-checkout-confirmation/equipment-checkout-confirmation.component';
import { AmbassadorEquipmentComponent } from './ambassador-equipment/ambassador-equipment.component';

// Routes for all components in equipment feature
const routes: Routes = [
  UserEquipmentComponent.Route,
  WaiverComponent.Route,
  EquipmentCheckoutConfirmationComponent.Route,
  AmbassadorEquipmentComponent.Route
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class EquipmentRoutingModule {}
