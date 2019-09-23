import { browser, by, element, ElementArrayFinder, ElementFinder, ExpectedConditions as EC } from "protractor";
import { HotelResult } from "../elements/HotelResult";
import { RailMap } from "../elements/RailMap";

export class HotelsResults {
  readonly railMap = new RailMap();
  
  static async loadResults() {
    const progressBar = element(by.className('Common-Results-ProgressBar'));
    await browser.wait(EC.invisibilityOf(progressBar));
    
    await browser.wait(
      EC.presenceOf(element(by.id('inline-3'))),
      15 * 1000,
      'Wait for advertisements to load'
    ).catch(error => console.error(error.message));
  }
  
  getSearchResult(index: number): HotelResult {
    return new HotelResult(
      this.getSearchResults().get(index)
    )
  }
  
  getExpandedSearchResult(index: number): HotelResult {
    const result = this.getSearchResults()
      .filter(elm => new HotelResult(elm).getTabsContainer().isDisplayed())
      .get(index);
    
    return new HotelResult(result);
  }
  
  getSearchResults(): ElementArrayFinder {
    const searchResultsContainer = element(by.id('searchResultsList'));
    browser.wait(EC.presenceOf(searchResultsContainer));
    browser.wait(EC.visibilityOf(searchResultsContainer));
    
    return element.all(by.className('Hotels-Results-HotelResultItem'));
  }
  
  getHorizontalFiltersContainer(): ElementFinder {
    return element(by.className(`horizontal-filters-wrapper`))
  }
  
}
