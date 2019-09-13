import {browser, ElementFinder, ExpectedConditions} from "protractor";

export default class CommonHelper {
    EC = ExpectedConditions;

    async waitForElementToBeVisible(element: ElementFinder): Promise<any> {
        await browser.wait(this.EC.visibilityOf(element), 5000)
    }
    async waitForElementToBeInvisible(element: ElementFinder): Promise<any> {
        await browser.wait(this.EC.invisibilityOf(element), 5000)
    }
    async waitForElementToBeClickable(element: ElementFinder): Promise<any> {
        await browser.wait(this.EC.elementToBeClickable(element), 5000)
    }
    async waitForURLToBeLoaded(url: string): Promise<any> {
        await browser.wait(this.EC.urlContains(browser.baseUrl +  url), 5000);
    }
}
