import { FlightsPageKayak } from "../brands/kayak/pages/flights";
import { FlightsResultsPageKayak } from "../brands/kayak/pages/flightsResults";
import { FlightsPageMomondo } from "../brands/momondo/pages/flights";
import { FlightsResultsPageMomondo } from "../brands/momondo/pages/flightsResults";
import { FlightsPage } from "../core/pages/flights";
import { FlightsResultsPage } from "../core/pages/flightsResults";

export class BrandPages {
  constructor(
    readonly flightsPage: FlightsPage,
    readonly flightsResultsPage: FlightsResultsPage,
  ) {
  }
}

export class BrandPagesFactory {
  static getPages(brand: string): BrandPages {
    switch (brand.toLowerCase()) {
      case 'kayak':
        return {
          flightsPage: new FlightsPageKayak(),
          flightsResultsPage: new FlightsResultsPageKayak()
        };
      
      case 'momondo':
        return {
          flightsPage: new FlightsPageMomondo(),
          flightsResultsPage: new FlightsResultsPageMomondo()
        };
      
      default:
        throw new Error(`No pages implementations found for brand: ${brand}`);
    }
  }
}
