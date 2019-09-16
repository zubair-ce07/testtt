import {browser, by, element, ElementFinder, ExpectedConditions} from "protractor";

export default class CommonHelper {
    EC = ExpectedConditions;
    async waitForURLToBeLoaded(url: string) {
        await browser.wait(this.EC.urlContains(browser.baseUrl+ url),2000);
    }
    async waitForElementToBeVisible(element: ElementFinder) {
        await browser.wait(this.EC.visibilityOf(element),2000);
    }
    async getCurrentURL(): Promise<string> {
        return await browser.getCurrentUrl();
    }
}
