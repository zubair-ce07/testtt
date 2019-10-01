import { FlightsResultsPageKayak } from "../brands/kayak/pages/flightsResults";
import { FlightsResultsPageMomondo } from "../brands/momondo/pages/flightsResults";
import { FlightsResultsPage } from "../core/pages/flightsResults";
import { BrandPageFactory } from "./brandPage";

export class FlightsResultsPageFactory implements BrandPageFactory<FlightsResultsPage> {
  create(brand: string): FlightsResultsPage {
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
