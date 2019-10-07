import { $, $$, browser, ElementArrayFinder, ExpectedConditions as EC } from "protractor";
import { FlightsResultsPage } from "../../../pages/flightsResultsPage";
import { SearchForm } from "../../../elements/forms/searchForm";

export class FlightsResultsPageKayak implements FlightsResultsPage {
  static async load(): Promise<void> {
    await browser.wait(EC.invisibilityOf($(`.Hotels-Results-PlaceholderList`)));
  }
  
  getSearchForm(): SearchForm {
    return undefined;
  }
  
  getSearchResults(): ElementArrayFinder {
    return $$(`.Base-Results-HorizonResult`);
  }
}
