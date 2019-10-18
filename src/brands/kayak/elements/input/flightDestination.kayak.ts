import { FlightDestination } from "../../../../core/elements/input/flightDestination";

export class FlightDestinationKayak implements FlightDestination {
  getDisplayText(): Promise<string> {
    return undefined;
  }
  
  isDisplayed(): Promise<boolean> {
    return undefined;
  }
  
  select(type: string): Promise<void> {
    return undefined;
  }
}
