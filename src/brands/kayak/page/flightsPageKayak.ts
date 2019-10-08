import { $, $$, browser, ElementArrayFinder, ElementFinder } from "protractor";
import { FlightsPage } from "../../../pages/flightsPage";
import { CompareTo } from "../../../elements/compareTo";
import { SearchPromo } from "../../../elements/promos/searchPromo";
import { Subscription } from "../../../elements/subscription";
import { Tile } from "../../../elements/tile";
import { SearchForm } from "../../../elements/forms/searchForm";
import { CompareToKayak } from "../elements/compareToKayak";
import { MobilePromoKayak } from "../elements/promos/mobilePromoKayak";
import { SearchFormKayak } from "../elements/forms/searchFormKayak";
import { SearchPromoKayak } from "../elements/promos/searchPromoKayak";
import { SubscriptionKayak } from "../elements/subscriptionKayak";
import { TileKayak } from "../elements/tileKayak";
import { HotelsSearchDialog } from "../../../elements/dialogs/hotelsSearchDialog";
import { HotelsSearchDialogKayak } from "../elements/dialogs/hotelsSearchDialogKayak";
import { DestinationSwitcher } from "../../../elements/switch/destinationSwitcher";
import { DestinationSwitcherKayak } from "../elements/switch/destinationSwitcherKayak";
import { FlightsResultsPageKayak } from "./flightsResultsPageKayak";
import { click, switchToNewTabIfOpened } from "../../../utils/specs.utils";
import { TilesFlightDialog } from "../../../elements/dialogs/tilesFlightDialog";
import { TilesHotelDialog } from "../../../elements/dialogs/tilesHotelDialog";
import { TilesFlightDialogKayak } from "../elements/dialogs/tilesFlightDialogKayak";
import { TilesHotelDialogKayak } from "../elements/dialogs/tilesHotelDialogKayak";
import { Promo } from "../../../elements/promos/promo";

export class FlightsPageKayak implements FlightsPage {
  getCompareTo(): CompareTo {
    return new CompareToKayak();
  }
  
  async getHeaderText(): Promise<string> {
    return $(`.Common-Frontdoor-PixelCoverPhoto`).$('h1').getText();
  }
  
  getMobilePromo(): Promo {
    return new MobilePromoKayak();
  }
  
  getSearchForm(): SearchForm {
    return new SearchFormKayak();
  }
  
  getSearchPromo(): SearchPromo {
    return new SearchPromoKayak();
  }
  
  getSlotAds(): ElementArrayFinder {
    return $$(`.col-fd-display-kn`);
  }
  
  getSubscription(): Subscription {
    return new SubscriptionKayak();
  }
  
  getTile(index: number): Tile {
    return new TileKayak(this.getTilesContainer().$$(`.tile`).get(index));
  }
  
  getTiles(): ElementArrayFinder {
    return this.getTilesContainer().$$(`.destinationTile`);
  }
  
  getURL(): string {
    return "https://www.kayak.com/horizon/sem/hotels/general/";
  }
  
  async visit(): Promise<void> {
    await browser.get(this.getURL());
  }
  
  getHotelsSearchDialog(): HotelsSearchDialog {
    return new HotelsSearchDialogKayak();
  }
  
  async search(): Promise<void> {
    const searchButton = $(`[name='searchform']`).$(`[id$='submit']`);
    await switchToNewTabIfOpened(click.bind(this, searchButton));
    await FlightsResultsPageKayak.load();
  }
  
  getSearchFormBanners(): ElementArrayFinder {
    return new ElementArrayFinder(browser, async () => [
      $(`[id$='leftImage']`),
      $(`[id$='rightImage']`)
    ]);
  }
  
  getDestinationSwitcher(): DestinationSwitcher {
    return new DestinationSwitcherKayak();
  }
  
  getTilesHotelDialog(): TilesHotelDialog {
    return new TilesHotelDialogKayak();
  }
  
  getTilesFlightDialog(): TilesFlightDialog {
    return new TilesFlightDialogKayak();
  }
  
  private getTilesContainer(): ElementFinder {
    return $(`.tilesWrapper`)
  }
  
}
