import { FlightLegDetails } from "../../../../core/elements/results/flightLegDetails";
import { FlightResultDialog } from "../../../../core/elements/dialogs/flightResultDialog";
import { FlightLegDetailsKayak } from "../results/flightLegDetails.kayak";

export class FlightResultDialogKayak implements FlightResultDialog {
  close(): Promise<void> {
    return undefined;
  }
  
  getDepartureDate(): Promise<string> {
    return undefined;
  }
  
  getFlightLeg(leg: number): FlightLegDetails {
    return new FlightLegDetailsKayak();
  }
  
  getPrice(): Promise<string> {
    return undefined;
  }
  
  getReturnDate(): Promise<string> {
    return undefined;
  }
  
  getTotalLegs(): Promise<number> {
    return undefined;
  }
  
  getTravellers(): Promise<string> {
    return undefined;
  }
  
  isDisplayed(): Promise<boolean> {
    return undefined;
  }
}
