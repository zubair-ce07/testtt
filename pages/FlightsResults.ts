import { browser, by, element } from "protractor";
import { waitForPageLoad } from "../utils/browser.util";
import { Passengers } from "../components/Passenger";
import { PriceAlertDialog } from "../components/Dialogs";
import { FlightResultsHeader } from "../components/Flights";
import { SearchForm } from "../components/SearchForm";

export class FlightsResultsPage {
  public form: SearchForm;
  public dialog: PriceAlertDialog;
  public header: FlightResultsHeader;
  
  constructor(private url: string) {
    this.dialog = new PriceAlertDialog();
    this.header = new FlightResultsHeader();
  }
  
  async load() {
    const url = await browser.getCurrentUrl();
    
    if (this.url !== url) {
      await browser.get(this.url);
      await browser.executeAsyncScript(waitForPageLoad());
    }
    
    await element(by.className('Flights-Search-FlightInlineSearchForm'))
      .getAttribute('id')
      .then(id => {
        this.form = new SearchForm(id);
        this.form.passengers = new Passengers(`${id}-travelers`);
      });
    
    await Promise.all([
      this.form.load(),
      this.header.load(),
    ]);
    
    await this.dialog.load()
  }
}
