import { FlightsResultsPageKayak } from "../brands/kayak/pages/flightsResultsPageKayak";
import { FlightsResultsPageMomondo } from "../brands/momondo/pages/flightsResultsPageMomondo";
import { FlightsResultsPage } from "../core/pages/flightsResultsPage";

export class FlightsResultsPageFactory {
  static create(): FlightsResultsPage {
    const brand = process.env.BRAND_NAME;
    
    switch (brand.toLowerCase()) {
      case 'kayak':
        return new FlightsResultsPageKayak();
      
      case 'momondo':
        return new FlightsResultsPageMomondo();
      
      default:
        throw new Error(`No FlightsResultsPage implementation found for brand: ${brand}`)
    }
  }
}
