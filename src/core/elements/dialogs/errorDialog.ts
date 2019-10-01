export interface ErrorDialog {
  closeDialog(): Promise<void>;
  
  getErrorMessages(): Promise<string[]>;
  
  isDisplayed(): Promise<boolean>;
}
