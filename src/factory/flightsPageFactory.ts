import { FlightsPageKayak } from "../brands/kayak/pages/flightsPageKayak";
import { FlightsPageMomondo } from "../brands/momondo/pages/flightsPageMomondo";
import { FlightsPage } from "../core/pages/flightsPage";

export class FlightsPageFactory {
  static create(): FlightsPage {
    const brand = process.env.BRAND_NAME;
    
    switch (brand.toLowerCase()) {
      case 'kayak':
        return new FlightsPageKayak();
      
      case 'momondo':
        return new FlightsPageMomondo();
      
      default:
        throw new Error(`No FlightsPage implementation found for brand: ${brand}`)
    }
  }
}
