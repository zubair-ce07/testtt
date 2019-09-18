import { by, element } from "protractor";

export class DateRange {
  getStartDateElement() {
    return element(by.css(`div[id$='-dateRangeInput-display-start']`))
  }
  
  getEndDateElement() {
    return element(by.css(`div[id$='-dateRangeInput-display-end']`))
  }
}
