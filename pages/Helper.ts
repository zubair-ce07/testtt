import {browser, ElementFinder, ExpectedConditions, ProtractorExpectedConditions} from "protractor";

export class Helper {
    EC: ProtractorExpectedConditions = ExpectedConditions;
    async getHotelIDNumber(marker: ElementFinder): Promise<string> {
        const hotelID = await marker.getAttribute('id');
        const hotelIDArray = hotelID.split('-');
        return hotelIDArray[1];
    }
    waitForElementToBeVisible(element: ElementFinder): any {
        browser.wait(this.EC.visibilityOf(element),10000)
    }
    waitForElementToBeInvisible(element: ElementFinder): any {
        browser.wait(this.EC.invisibilityOf(element),5000)
    }
    waitForElementToBeClickable(element: ElementFinder): any {
        browser.wait(this.EC.elementToBeClickable(element),5000)
    }
}