import {browser, by, element} from "protractor";
import CommonHelper from "../helper/CommonHelper";

export default class CarResultPage {
    commonHelperObj = new CommonHelper();

    carResultList = element(by.css('.js-result'));
    carResults = element.all(by.css('.js-result'));
    map = element(by.css("div[id*='-map']"));

    async isCarResultsLoaded(): Promise<boolean> {
        const allWindows = await browser.getAllWindowHandles();
        await browser.switchTo().window(allWindows[1]);
        await this.commonHelperObj.waitForElementToBeVisible(this.carResultList);
        return await this.carResultList.isDisplayed();
    }
    async getCarResultCount(): Promise<number> {
        await this.commonHelperObj.waitForElementToBeVisible(this.carResults.first());
        return await this.carResults.count();
    }
    async isMapVisible(): Promise<boolean> {
        return this.map.isDisplayed();
    }
}