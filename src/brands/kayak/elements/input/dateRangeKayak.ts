import { DateRange } from "../../../../elements/input/dateRange";
import { $ } from "protractor";

export class DateRangeKayak implements DateRange {
  select(start: Date, end: Date): Promise<void> {
    return undefined;
  }
  
  async getEndDateText(): Promise<string> {
    return $(`div[id$='dateRangeInput-display-end-inner']`).getText();
  }
  
  async getStartDateText(): Promise<string> {
    return $(`div[id$='dateRangeInput-display-start-inner']`).getText();
  }
}
