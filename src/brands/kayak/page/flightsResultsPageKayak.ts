import { FlightsResultsPage } from "../../../pages/flightsResultsPage";
import { SearchForm } from "../../../elements/forms/searchForm";
import { ElementArrayFinder } from "protractor";

export class FlightsResultsPageKayak implements FlightsResultsPage {
  getSearchForm(): SearchForm {
    return undefined;
  }
  
  getSearchResults(): ElementArrayFinder {
    return undefined;
  }
}
