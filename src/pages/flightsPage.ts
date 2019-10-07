import { ElementArrayFinder } from "protractor";

import { CompareTo } from "../elements/compareTo";
import { SearchPromo } from "../elements/promos/searchPromo";
import { MobilePromo } from "../elements/promos/mobilePromo";
import { Tile } from "../elements/tile";
import { Subscription } from "../elements/subscription";
import { Page } from "./page";
import { SearchForm } from "../elements/forms/searchForm";
import { FlightsSearchDialog } from "../elements/dialogs/flightsSearchDialog";
import { HotelsSearchDialog } from "../elements/dialogs/hotelsSearchDialog";
import { DestinationSwitcher } from "../elements/switch/destinationSwitcher";

export interface FlightsPage extends Page {
  search(): Promise<void>;
  
  getTile(index: number): Tile;
  
  getTiles(): ElementArrayFinder;
  
  getSlotAds(): ElementArrayFinder;
  
  getCompareTo(): CompareTo;
  
  getSearchForm(): SearchForm;
  
  getHeaderText(): Promise<string>
  
  getSearchPromo(): SearchPromo;
  
  getMobilePromo(): MobilePromo;
  
  getSubscription(): Subscription;
  
  getSearchFormBanners(): ElementArrayFinder;
  
  getHotelsSearchOverlay(): HotelsSearchDialog;
  
  getDestinationSwitcher(): DestinationSwitcher;
  
  getFlightsSearchOverlay(): FlightsSearchDialog;
}
