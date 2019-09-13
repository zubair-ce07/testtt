import { browser, by, element } from "protractor";
import { waitForPageLoad } from "../utils/browser.util";
import { SearchForm } from "../components/SearchForm";

export class FlightsPage {
  public form: SearchForm;
  
  async load() {
    await browser.get('https://www.kayak.com');
    await browser.executeAsyncScript(waitForPageLoad());
  
    const form = element(by.className('Base-Search-SearchForm'));
    const id = await form.getAttribute('id');
    this.form = new SearchForm(id);
  
    return this.form.load();
  }
}

