export interface DatePicker {
  select(date: Date): Promise<void>;
  
  isDisplayed(): Promise<boolean>;
  
  getDisplayText(): Promise<string>;
}
