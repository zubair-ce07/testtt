import {by, element, ElementFinder} from "protractor";
import CommonHelper from "../helper/CommonHelper";

export default class KayakHomepage {
    commonHelperObj = new CommonHelper();

    hotelsBtn = element(by.css('.TopNavLinks__vertical--hotels'));
    flightsBtn = element(by.css('.TopNavLinks__vertical--flights'));
    carsBtn = element(by.css('.TopNavLinks__vertical--cars'));

    async isFlightsBtnVisible(): Promise<boolean> {
        return await this.flightsBtn.isDisplayed();
    }
    async isHotelsBtnVisible(): Promise<boolean> {
        return await this.hotelsBtn.isDisplayed();
    }
    async isCarsBtnVisible(): Promise<boolean> {
        return await this.carsBtn.isDisplayed();
    }
    async clickFlightsBtn(): Promise<void> {
        await this.flightsBtn.click();
    }
    async isFlightsBtnHighlighted(): Promise<boolean> {
        return await this.isHighlighted(this.flightsBtn);
    }
    async clickHotelsBtn(): Promise<void> {
        await this.clickBtn(this.hotelsBtn);
    }
    async isHotelsBtnHighlighted(): Promise<boolean> {
        return await this.isHighlighted(this.hotelsBtn);
    }
    async clickCarsBtn(): Promise<void> {
        await this.clickBtn(this.carsBtn);
    }
    async isCarsBtnHighlighted(): Promise<boolean> {
        return await this.isHighlighted(this.carsBtn);
    }

    async isHighlighted(element: ElementFinder): Promise<boolean> {
        const elementClass = await element.getAttribute('class');
        return elementClass.includes('active');
    }
    async clickBtn(btn: ElementFinder): Promise<void> {
        const btnClassName = await btn.getAttribute('class');
        await btn.click();
        await this.commonHelperObj.waitForElementToBeActive(btnClassName);
    }
}
