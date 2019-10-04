import { SearchForm } from "../elements/forms/searchForm";
import { ElementArrayFinder } from "protractor";

export interface FlightsResultsPage {
  getSearchForm(): SearchForm;
  
  getSearchResults(): ElementArrayFinder;
}
