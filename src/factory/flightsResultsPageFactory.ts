import { FlightsResultsPage } from "../pages/flightsResultsPage";
import { FlightsResultsPageKayak } from "../brands/kayak/page/flightsResultsPageKayak";

export class FlightsResultsPageFactory {
  static create(): FlightsResultsPage {
    const BRAND_NAME = process.env.BRAND_NAME;
    
    switch (BRAND_NAME) {
      case 'kayak':
        return new FlightsResultsPageKayak();
      
      default:
        throw new Error(`No Flights page implementation found for brand ${BRAND_NAME}`)
    }
  }
}
