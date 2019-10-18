import { FlightsResultsPage } from "../../../core/pages/flightsResultsPage";
import { FlightResult } from "../../../core/elements/results/flightResult";
import { FlightResultKayak } from "../elements/results/flightResult.kayak";
import { FlightResultsSummary } from "../../../core/elements/results/flightResultsSummary";
import { FlightResultsSummaryKayak } from "../elements/results/flightResultsSummary.kayak";

export class FlightsResultsPageKayak implements FlightsResultsPage {
  getFlightResult(index: number): FlightResult {
    return new FlightResultKayak();
  }
  
  getFlightResults(): Promise<FlightResult[]> {
    return undefined;
  }
  
  getSearchSummary(): FlightResultsSummary {
    return new FlightResultsSummaryKayak();
  }
  
  isLoaded(): Promise<boolean> {
    return undefined;
  }
  
  loadResults(): Promise<void> {
    return undefined;
  }
}
