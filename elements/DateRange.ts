import { by, element, ElementFinder } from "protractor";

export class DateRange {
  getStartDateElement(): ElementFinder {
    return element(by.css(`div[id$='-dateRangeInput-display-start']`))
  }
  
  getEndDateElement(): ElementFinder {
    return element(by.css(`div[id$='-dateRangeInput-display-end']`))
  }
}
