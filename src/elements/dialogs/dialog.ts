export interface Dialog {
  isDisplayed(): Promise<boolean>
  
  close(): Promise<void>;
}
