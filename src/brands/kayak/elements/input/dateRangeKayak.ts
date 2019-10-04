import { DateRange } from "../../../../elements/input/dateRange";

export class DateRangeKayak implements DateRange {
  select(start: Date, end: Date): Promise<void> {
    return undefined;
  }
  
  getEndDateText(): Promise<string> {
    return undefined;
  }
  
  getStartDateText(): Promise<string> {
    return undefined;
  }
}
