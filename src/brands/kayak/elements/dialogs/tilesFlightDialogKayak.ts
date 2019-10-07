import { TilesFlightDialog } from "../../../../elements/dialogs/tilesFlightDialog";
import { $, browser, ElementFinder, ExpectedConditions as EC } from "protractor";

export class TilesFlightDialogKayak implements TilesFlightDialog {
  async close(): Promise<void> {
    const closeButton = this.getDialogContainer().$(`button[id$='destination_tiles_flight_dialog-dialog-close']`);
    await closeButton.click();
    await browser.wait(EC.invisibilityOf(this.getDialogContainer()));
  }
  
  async isDisplayed(): Promise<boolean> {
    return this.getDialogContainer().isPresent();
  }
  
  private getDialogContainer(): ElementFinder {
    return $(`.Sem-Flights-Search-SEMFlightSearchDialog`)
  }
}
