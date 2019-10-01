import { by, element, ElementFinder } from "protractor";
import { ErrorDialog } from "../../../../core/elements/dialogs/errorDialog";

export class ErrorDialogKayak implements ErrorDialog {
  async closeDialog(): Promise<void> {
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
