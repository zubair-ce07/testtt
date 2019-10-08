export interface Promo {
  isDisplayed(): Promise<boolean>;
  
  focus(): Promise<void>;
}
