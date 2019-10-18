import { FlightOrigin } from "../input/flightOrigin";
import { FlightDestination } from "../input/flightDestination";
import { DatePicker } from "../input/datePicker";

export interface FlightForm {
  getOrigin(): FlightOrigin;
  
  getDestination(): FlightDestination;
  
  getDatePicker(): DatePicker;
}
