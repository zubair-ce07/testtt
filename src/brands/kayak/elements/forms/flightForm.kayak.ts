import { DatePicker } from "../../../../core/elements/input/datePicker";
import { FlightForm } from "../../../../core/elements/forms/flightForm";
import { FlightDestination } from "../../../../core/elements/input/flightDestination";
import { FlightOrigin } from "../../../../core/elements/input/flightOrigin";
import { DatePickerKayak } from "../input/datePicker.kayak";
import { FlightDestinationKayak } from "../input/flightDestination.kayak";
import { FlightOriginKayak } from "../input/flightOrigin.kayak";

export class FlightFormKayak implements FlightForm {
  getDatePicker(): DatePicker {
    return new DatePickerKayak();
  }
  
  getDestination(): FlightDestination {
    return new FlightDestinationKayak();
  }
  
  getOrigin(): FlightOrigin {
    return new FlightOriginKayak();
  }
}
