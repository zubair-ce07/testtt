import {Helper} from "./Helper";
import HotelSearchResultsElements from '../pageElements/HotelSearchResultsElements'

export class HotelSearchResultsPage {
    hotelsSearchResultsElementsObj = new HotelSearchResultsElements();
    helperObj = new Helper();

    async isHotelsResultPageLoaded(): Promise<boolean> {
        const hotelsSearchResults = await this.hotelsSearchResultsElementsObj.getHotelsSearchResults();
        this.helperObj.waitForElementToBeVisible(hotelsSearchResults);
        return hotelsSearchResults.isDisplayed()
    }
    async getTotalNumOfHotelsResults(): Promise<number> {
        return this.hotelsSearchResultsElementsObj.getAllHotelsResults().count();
    }
    async openHotelDetailsDropdown(): Promise<void> {
        await this.hotelsSearchResultsElementsObj.getFirstHotelName().click();
    }
    async isHotelDetailsDropdownVisible(): Promise<boolean> {
        const hotelDetailsDropdown = this.hotelsSearchResultsElementsObj.getHotelDetailsDropdown();
        this.helperObj.waitForElementToBeVisible(hotelDetailsDropdown);
        return hotelDetailsDropdown.isDisplayed();
    }
    async isDetailsTabPhotosVisible(): Promise<boolean> {
        return this.hotelsSearchResultsElementsObj.getPhotosInDetailsTab().isDisplayed();
    }
    async isMapInMapTabVisible(): Promise<boolean> {
        await this.hotelsSearchResultsElementsObj.getMapTabBtn().click();
        const map = this.hotelsSearchResultsElementsObj.getMapInMapTab();
        this.helperObj.waitForElementToBeVisible(map);
        return map.isDisplayed();
    }
    async isReviewsInReviewsTabVisible(): Promise<boolean> {
        await this.hotelsSearchResultsElementsObj.getReviewsTabBtn().click();
        const reviews = this.hotelsSearchResultsElementsObj.getReviewsInReviewsTab();
        this.helperObj.waitForElementToBeVisible(reviews);
        return reviews.isDisplayed();
    }
    async isRatesInRatesTabVisible(): Promise<boolean> {
        await this.hotelsSearchResultsElementsObj.getRatesTabBtn().click();
        const rates = this.hotelsSearchResultsElementsObj.getRatesInRatesTab();
        this.helperObj.waitForElementToBeVisible(rates);
        return rates.isDisplayed();
    }
}