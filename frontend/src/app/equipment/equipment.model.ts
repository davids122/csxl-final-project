/**
 * The Equipment Model defines the shape of Equipment data
 * retrieved from the Equipment Service and API.
 */

export interface Equipment {
  id: number;
  equipment_id: number;
  model: string;
  equipment_image: string;
  condition: number;
  is_checked_out: boolean;
}
