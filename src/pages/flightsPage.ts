import { ElementArrayFinder } from "protractor";

import { CompareTo } from "../elements/compareTo";
import { SearchPromo } from "../elements/promos/searchPromo";
import { Tile } from "../elements/tile";
import { Subscription } from "../elements/subscription";
import { Page } from "./page";
import { SearchForm } from "../elements/forms/searchForm";
import { HotelsSearchDialog } from "../elements/dialogs/hotelsSearchDialog";
import { DestinationSwitcher } from "../elements/switch/destinationSwitcher";
import { TilesHotelDialog } from "../elements/dialogs/tilesHotelDialog";
import { TilesFlightDialog } from "../elements/dialogs/tilesFlightDialog";
import { Promo } from "../elements/promos/promo";

export interface FlightsPage extends Page {
  search(): Promise<void>;
  
  getTile(index: number): Tile;
  
  getTiles(): ElementArrayFinder;
  
  getSlotAds(): ElementArrayFinder;
  
  getCompareTo(): CompareTo;
  
  getSearchForm(): SearchForm;
  
  getHeaderText(): Promise<string>
  
  getSearchPromo(): SearchPromo;
  
  getMobilePromo(): Promo;
  
  getSubscription(): Subscription;
  
  getTilesHotelDialog(): TilesHotelDialog;
  
  getTilesFlightDialog(): TilesFlightDialog;
  
  getSearchFormBanners(): ElementArrayFinder;
  
  getHotelsSearchDialog(): HotelsSearchDialog;
  
  getDestinationSwitcher(): DestinationSwitcher;
  
}
