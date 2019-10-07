import { TilesHotelDialog } from "../../../../elements/dialogs/tilesHotelDialog";
import { $, browser, ElementFinder, ExpectedConditions as EC } from "protractor";
import { click } from "../../../../utils/specs.utils";

export class TilesHotelDialogKayak implements TilesHotelDialog {
  async close(): Promise<void> {
    const closeButton = this.getDialogContainer().$(`button[id$='destination_tiles_hotel_dialog-dialog-close']`);
    await click(closeButton);
    await browser.wait(EC.invisibilityOf(this.getDialogContainer()));
  }
  
  async isDisplayed(): Promise<boolean> {
    return this.getDialogContainer().isPresent();
  }
  
  private getDialogContainer(): ElementFinder {
    return $(`.Sem-Hotels-Search-SEMHotelSearchDialog`)
  }
}
