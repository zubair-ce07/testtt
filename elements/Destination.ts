import { browser, by, element, ExpectedConditions as EC } from "protractor"

export class Destination {
  getDialog() {
    return element.all(by.css(`div[id$='-location-display']`)).first();
  }
  
  getDialogWindow() {
    return element.all(by.css(`div[id$='-location-smarty-window']`)).first();
  }
  
  getInputElement() {
    return element.all(by.css(`input[id$='-location']`)).first();
  }
  
  getSearchResultsElement() {
    return element.all(by.css(`div[id$='-location-smartbox-dropdown']`)).first();
  }
  
  type(text: string) {
    const dialog = this.getDialog();
    const dialogWindow = this.getDialogWindow();
    
    browser.wait(EC.presenceOf(dialog));
    browser.wait(EC.visibilityOf(dialog));
    browser.wait(EC.elementToBeClickable(dialog));
    dialog.click();
    
    browser.wait(EC.visibilityOf(dialogWindow));
    
    const input = this.getInputElement();
    browser.wait(EC.presenceOf(input));
    browser.wait(EC.visibilityOf(input));
    
    input.sendKeys(text);
    
    browser.wait(EC.textToBePresentInElementValue(input, text));
  }
  
  selectSearchResult(index: number) {
    const results = this.getSearchResultsElement();
    browser.wait(EC.presenceOf(results));
    browser.wait(EC.visibilityOf(results));
    
    const resultsList = results.all(by.tagName('li'));
    const result = resultsList.get(index);
    
    browser.wait(EC.presenceOf(result));
    browser.wait(EC.visibilityOf(result));
    browser.wait(EC.elementToBeClickable(result));
    
    result.click();
    expect(EC.invisibilityOf(results));
  }
  
}
