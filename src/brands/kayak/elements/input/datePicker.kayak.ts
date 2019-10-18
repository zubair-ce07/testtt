import { DatePicker } from "../../../../core/elements/input/datePicker";

export class DatePickerKayak implements DatePicker {
  getDisplayText(): Promise<string> {
    return undefined;
  }
  
  isDisplayed(): Promise<boolean> {
    return undefined;
  }
  
  select(date: Date): Promise<void> {
    return undefined;
  }
}
