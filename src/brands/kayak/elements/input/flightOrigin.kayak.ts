import { FlightOrigin } from "../../../../core/elements/input/flightOrigin";

export class FlightOriginKayak implements FlightOrigin {
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
