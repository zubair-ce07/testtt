import { FlightsPageKayak } from "../brands/kayak/pages/flightsPageKayak";
import { FlightsPageMomondo } from "../brands/momondo/pages/flightsPageMomondo";
import { FlightsPage } from "../core/pages/flightsPage";
import { PageFactory } from "./pageFactory";

export class FlightsPageFactory implements PageFactory<FlightsPage> {
  create(brand: string): FlightsPage {
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
