import { FlightResult } from "../../../../core/elements/results/flightResult";
import { FlightResultDialog } from "../../../../core/elements/dialogs/flightResultDialog";
import { FlightResultDialogKayak } from "../dialogs/flightResultDialog.kayak";
import { FlightLeg } from "../../../../core/elements/results/flightLeg";
import { FlightLegKayak } from "./flightLeg.kayak";

export class FlightResultKayak implements FlightResult {
  click(): Promise<void> {
    return undefined;
  }
  
  getDialog(): FlightResultDialog {
    return new FlightResultDialogKayak();
  }
  
  getFlightLeg(leg: Number): FlightLeg {
    return new FlightLegKayak();
  }
  
  getPrice(): Promise<string> {
    return undefined;
  }
  
  getTotalLegs(): Promise<number> {
    return undefined;
  }
}
