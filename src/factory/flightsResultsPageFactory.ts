import { FlightsResultsPageKayak } from "../brands/kayak/pages/flightsResultsPageKayak";
import { FlightsResultsPageMomondo } from "../brands/momondo/pages/flightsResultsPageMomondo";
import { FlightsResultsPage } from "../core/pages/flightsResultsPage";
import { PageFactory } from "./pageFactory";

export class FlightsResultsPageFactory implements PageFactory<FlightsResultsPage> {
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
