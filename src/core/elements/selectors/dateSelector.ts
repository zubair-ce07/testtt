export interface DateSelector {
  selectDate(date: Date): Promise<void>;
  
  getDisplayText(): Promise<string>;
}
