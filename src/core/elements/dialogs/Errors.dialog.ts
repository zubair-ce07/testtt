export interface ErrorsDialog {
  clickOkay(): Promise<void>;
  
  getErrorMessages(): Promise<string[]>;
  
  isDisplayed(): Promise<boolean>;
}
