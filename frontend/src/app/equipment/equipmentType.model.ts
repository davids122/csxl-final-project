/**
 * The EquipmentType Model defines the shape of the data that is going to be displayed
 * on the frontend user equipment component. This is necessary in order to display an
 * containing an count for how many of each type of equipment are avaialable.
 */

export interface EquipmentType {
  model: string;
  num_available: number;
  equipment_img_URL: string;
}
