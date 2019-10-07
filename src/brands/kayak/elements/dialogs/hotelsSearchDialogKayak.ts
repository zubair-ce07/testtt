import { $, browser, ElementFinder, ExpectedConditions as EC } from "protractor";
import { HotelsSearchDialog } from "../../../../elements/dialogs/hotelsSearchDialog";

export class HotelsSearchDialogKayak implements HotelsSearchDialog {
  async close(): Promise<void> {
    await $(`button[id$='searchDialog-dialog-close']`).click();
    await browser.wait(EC.invisibilityOf(this.getDialogContainer()));
  }
  
  async isDisplayed(): Promise<boolean> {
    return this.getDialogContainer().isDisplayed();
  }
  
  private getDialogContainer(): ElementFinder {
    return $(`div[id$='searchDialog-dialog']`)
  }
}
