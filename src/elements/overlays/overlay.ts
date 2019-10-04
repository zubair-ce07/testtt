export interface Overlay {
  isDisplayed(): Promise<boolean>
  
  close(): Promise<void>;
}
