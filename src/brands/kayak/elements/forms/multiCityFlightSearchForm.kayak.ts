import { MultiCityFlightSearchForm } from "../../../../core/elements/forms/multiCityFlightSearchForm";
import { FlightForm } from "../../../../core/elements/forms/flightForm";

export class MultiCityFlightSearchFormKayak implements MultiCityFlightSearchForm {
  addFlightLegs(count: number): Promise<unknown> {
    return undefined;
  }
  
  getFlightLeg(leg: number): FlightForm {
    return undefined;
  }
  
  getFlightLegs(): Promise<FlightForm[]> {
    return undefined;
  }
  
  removeFlightLegs(count: number): Promise<unknown> {
    return undefined;
  }
}
