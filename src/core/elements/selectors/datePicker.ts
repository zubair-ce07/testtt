export interface DatePicker {
  selectDate(date: Date): Promise<void>;
  
  getDisplayText(): Promise<string>;
}
