/**
 * The staged checkout request model defines the shape of the data to be represented in the ambassadors view
 * of the staging area for checkout requests.
 */
export interface StagedCheckoutRequestModel {
  user_name: String;
  model: String;
  id_choices: Number[] | null;
  selected_id: Number | null;
  pid: Number;
}
