export interface DateRange {
  select(start: Date, end: Date): Promise<void>;
  
  getStartDateText(): Promise<string>;
  
  getEndDateText(): Promise<string>;
}
