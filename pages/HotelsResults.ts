import { browser, by, element, ElementArrayFinder, ElementFinder, ExpectedConditions as EC } from "protractor";
import { HotelResult } from "../elements/HotelResult";
import { RailMap } from "../elements/RailMap";

export class HotelsResults {
  readonly railMap = new RailMap();
  
  load(): void {
    const progressBar = element(by.className('Common-Results-ProgressBar'));
    browser.wait(EC.invisibilityOf(progressBar));
  }
  
  getSearchResult(index: number): HotelResult {
    return new HotelResult(
      this.getSearchResults().get(index)
    )
  }
  
  getExpandedSearchResult(index: number): HotelResult {
    const result = this.getSearchResults()
      .filter(elm => new HotelResult(elm).isDetailsWrapperDisplayed())
      .get(index);
    
    return new HotelResult(result);
  }
  
  getSearchResults(): ElementArrayFinder {
    const elm = element(by.id('searchResultsList'));
    browser.wait(EC.presenceOf(elm));
    browser.wait(EC.visibilityOf(elm));
    
    return element.all(by.className('Hotels-Results-HotelResultItem'));
  }
  
  getHorizontalFiltersContainer(): ElementFinder {
    return element(by.className(`horizontal-filters-wrapper`))
  }
  
}
