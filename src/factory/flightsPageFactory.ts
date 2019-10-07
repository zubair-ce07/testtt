import { FlightsPage } from "../pages/flightsPage";
import { FlightsPageKayak } from "../brands/kayak/page/flightsPageKayak";

export class FlightsPageFactory {
  static create(): FlightsPage {
    const BRAND_NAME = process.env.BRAND_NAME;
    
    switch (BRAND_NAME) {
      case 'kayak':
        return new FlightsPageKayak();
      
      default:
        throw new Error(`No Flights page implementation found for brand ${BRAND_NAME}`)
    }
  }
}
