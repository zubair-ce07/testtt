import { FlightsPageKayak } from "../brands/kayak/pages/flights";
import { FlightsPageMomondo } from "../brands/momondo/pages/flights";
import { FlightsPage } from "../core/pages/flights";
import { BrandPageFactory } from "./brandPage";

export class FlightsPageFactory implements BrandPageFactory<FlightsPage> {
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
