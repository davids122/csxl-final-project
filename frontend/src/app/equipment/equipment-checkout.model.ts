/**
 * The Equipment Checkout Model defines the shape of Equipment Checkouts
 * retrieved from the Equipment Service and API.
 */

export interface EquipmentCheckoutModel {
  user_name: String;
  pid: Number;
  equipment_id: Number;
  model: String;
  is_active: Boolean;
  started_at: Date;
  end_at: Date;
}
