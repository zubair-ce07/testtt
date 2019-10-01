export interface ErrorDialog {
  clickOkay(): Promise<void>;
  
  getErrorMessages(): Promise<string[]>;
  
  isDisplayed(): Promise<boolean>;
}
