import { FlightsPage } from "../../../pages/flightsPage";
import { CompareTo } from "../../../elements/compareTo";
import { MobilePromo } from "../../../elements/promos/mobilePromo";
import { SearchPromo } from "../../../elements/promos/searchPromo";
import { ElementArrayFinder } from "protractor";
import { Subscription } from "../../../elements/subscription";
import { Tile } from "../../../elements/tile";
import { SearchForm } from "../../../elements/forms/searchForm";
import { CompareToKayak } from "../elements/compareToKayak";
import { MobilePromoKayak } from "../elements/promos/mobilePromoKayak";
import { SearchFormKayak } from "../elements/forms/searchFormKayak";
import { SearchPromoKayak } from "../elements/promos/searchPromoKayak";
import { SubscriptionKayak } from "../elements/subscriptionKayak";
import { TileKayak } from "../elements/tileKayak";
import { FlightsSearchOverlay } from "../../../elements/overlays/flightsSearchOverlay";
import { FlightsSearchOverlayKayak } from "../elements/overlays/flightsSearchOverlayKayak";
import { HotelsSearchOverlay } from "../../../elements/overlays/hotelsSearchOverlay";
import { HotelsSearchOverlayKayak } from "../elements/overlays/hotelsSearchOverlayKayak";
import { DestinationSwitcher } from "../../../elements/switch/destinationSwitcher";

export class FlightsPageKayak implements FlightsPage {
  getCompareTo(): CompareTo {
    return new CompareToKayak();
  }
  
  getHeaderText(): Promise<string> {
    return undefined;
  }
  
  getMobilePromo(): MobilePromo {
    return new MobilePromoKayak();
  }
  
  getSearchForm(): SearchForm {
    return new SearchFormKayak();
  }
  
  getSearchPromo(): SearchPromo {
    return new SearchPromoKayak();
  }
  
  getSlotAds(): ElementArrayFinder {
    return undefined;
  }
  
  getSubscription(): Subscription {
    return new SubscriptionKayak();
  }
  
  getTile(index: number): Tile {
    return new TileKayak(index);
  }
  
  getTiles(): ElementArrayFinder {
    return undefined;
  }
  
  getURL(): string {
    return "";
  }
  
  visit(): Promise<void> {
    return undefined;
  }
  
  getHotelsSearchOverlay(): HotelsSearchOverlay {
    return new HotelsSearchOverlayKayak();
  }
  
  getFlightsSearchOverlay(): FlightsSearchOverlay {
    return new FlightsSearchOverlayKayak();
  }
  
  search(): Promise<void> {
    return undefined;
  }
  
  getSearchFormBanners(): ElementArrayFinder {
    return undefined;
  }
  
  getDestinationSwitcher(): DestinationSwitcher {
    return undefined;
  }
  
}
