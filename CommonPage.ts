import {browser, $, element, by, protractor, promise, ElementFinder, ElementArrayFinder, ProtractorExpectedConditions} from 'protractor';

export class CommonPage {
  
    async waitUntillElementAppears(element: any): Promise<void> {
        let until: ProtractorExpectedConditions = await protractor.ExpectedConditions; 
        browser.wait(
        until.visibilityOf(element),
        30000, 'element taking too long to appear in the DOM');
    }

    patternToBePresentInElement(elementFinder: ElementFinder, pattern: RegExp) {
        let EC = protractor.ExpectedConditions;
        let matchesPattern = function() {
            return elementFinder.getText().then(function(actualText: string) {
            return actualText.search(pattern) !== -1;
            });
        };
        return EC.and(EC.presenceOf(elementFinder), matchesPattern);
    };
    
}