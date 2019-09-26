import { by, element, ElementFinder } from "protractor";
import { ErrorsDialog } from "../../../../core/elements/dialogs";

export class ErrorsDialogKayak implements ErrorsDialog {
  async clickOkay(): Promise<void> {
    await this.getErrorContainer().element(by.className(`errorDialogCloseButton`)).click();
  }
  
  async getErrorMessages(): Promise<string[]> {
    return element(by.className(`errorMessages`)).all(by.tagName('li')).map(li => li.getText());
  }
  
  async isDisplayed(): Promise<boolean> {
    return this.getErrorContainer().isDisplayed();
  }
  
  getErrorContainer(): ElementFinder {
    return element(by.className(`Common-Errors-ErrorDialog-Dialog`));
  }
  
}
