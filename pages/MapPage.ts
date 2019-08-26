import {browser} from "protractor";
import {Helper} from "./Helper";
import MapPageElements from "../pageElements/MapPageElements";

export class MapPage {
    helperObj = new Helper();
    mapPageElements = new MapPageElements();
    HOTEL_MARKER_ID: string = '';

    async clickShowMap(): Promise<void> {
        const showMapBtn = await this.mapPageElements.getShowMapBtn();
        this.helperObj.waitForElementToBeClickable(showMapBtn);
        showMapBtn.click();
    }
    async isMainMapViewVisible(): Promise<boolean> {
        const mainMap = await this.mapPageElements.getMainMap();
        this.helperObj.waitForElementToBeVisible(mainMap);
        return mainMap.isDisplayed();
    }
    async isHorizontalFiltersVisible(): Promise<boolean> {
        const horizontalFilters = await this.mapPageElements.getHorizontalFilters();
        this.helperObj.waitForElementToBeVisible(horizontalFilters);
        return horizontalFilters.isDisplayed();
    }
    async isHotelInfoVisible(): Promise<boolean> {
        const hotelMarker = this.mapPageElements.getHotelMarker();
        browser.actions().mouseMove(hotelMarker).perform();
        const hotelIDNumber = await this.helperObj.getHotelIDNumber(hotelMarker);
        const hotelInfoHoverCard = await this.mapPageElements.getHotelInfoHoverCard(hotelIDNumber);
        this.helperObj.waitForElementToBeVisible(hotelInfoHoverCard);
        return hotelInfoHoverCard.isDisplayed();
    }
    async isHotelCardVisible(): Promise<boolean> {
        const hotelMarker = this.mapPageElements.getHotelMarker();
        await hotelMarker.click();
        this.HOTEL_MARKER_ID = await this.helperObj.getHotelIDNumber(hotelMarker);
        const hotelCard = await this.mapPageElements.getHotelCard(this.HOTEL_MARKER_ID);
        this.helperObj.waitForElementToBeVisible(hotelCard);
        return hotelCard.isDisplayed();
    }
    async getBookingProviderName(): Promise<string> {
        const bookingProvider = await this.mapPageElements.getBookingProvider(this.HOTEL_MARKER_ID);
        return bookingProvider.getText();
    }
    async clickViewDealBtn(): Promise<void> {
        const viewDealBtn = await this.mapPageElements.getViewDealBtn(this.HOTEL_MARKER_ID);
        this.helperObj.waitForElementToBeClickable(viewDealBtn);
        viewDealBtn.click();
    }
    async isBookingProviderPageOpened(providerName: string): Promise<string> {
        await browser.wait(this.helperObj.EC.urlContains(providerName), 10000);
        return await browser.getCurrentUrl();
    }
}