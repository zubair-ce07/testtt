import {browser} from "protractor";
import HotelsFrontPageElements from "../pageElements/HotelsFrontPageElements";
import {Helper} from "./Helper";

export default class HotelsFrontPage {
    helper = new Helper();
    hotelsFrontPageElementsObj = new HotelsFrontPageElements();
    KAYAKHomePageAddress: string = 'https://www.kayak.com/';

    async loadKAYAKHomePage() {
        await browser.get(this.KAYAKHomePageAddress);
    }
    async goToHotelsFrontPage(): Promise<void> {
        await this.hotelsFrontPageElementsObj.getHotelsBtn().click();
    }
    async isHotelsOriginVisible(): Promise<boolean> {
        return this.hotelsFrontPageElementsObj.getHotelsOriginField().isDisplayed();
    }
    async isHotelsStartDateVisible(): Promise<boolean> {
        return this.hotelsFrontPageElementsObj.getHotelsStartDateField().isDisplayed();
    }
    async isHotelsEndDateVisible(): Promise<boolean> {
        return this.hotelsFrontPageElementsObj.getHotelsEndDateField().isDisplayed();
    }
    async getGuestFieldText(): Promise<string> {
        return this.hotelsFrontPageElementsObj.getHotelsGuestField().getText();
    }
    async searchByNewHotelsOrigin(): Promise<void> {
        this.hotelsFrontPageElementsObj.getHotelsOriginField().click();
        this.hotelsFrontPageElementsObj.getHotelsOriginInputField().sendKeys('BCN');
        const originDropdown = this.hotelsFrontPageElementsObj.getOriginDropdown();
        this.helper.waitForElementToBeVisible(originDropdown);
        this.hotelsFrontPageElementsObj.getFirstResultOfOriginDropdown().click();
        this.helper.waitForElementToBeInvisible(originDropdown);
        const searchHotelsBtn = this.hotelsFrontPageElementsObj.getSearchHotelsBtn();
        this.helper.waitForElementToBeClickable(searchHotelsBtn);
        searchHotelsBtn.click();
        browser.sleep(20000);
    }
}