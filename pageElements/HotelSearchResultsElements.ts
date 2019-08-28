import {by, element, ElementArrayFinder, ElementFinder} from "protractor";

export default class HotelSearchResultsElements {
    hotelsSearchResult: ElementFinder = element(by.css("div[id='searchResultsList']"));
    allSearchedHotels: ElementArrayFinder = element.all(by.css('.resultWrapper'));
    allHotelNames: ElementArrayFinder = element.all(by.css("button[id*='-info-title']"));
    allHotelDetailsDropdown: ElementArrayFinder = element.all(by.css(".detailsContent"));
    hotelDetailsDropDownTabList: ElementFinder = this.allHotelDetailsDropdown.first();
    activeTabContent: ElementFinder = this.hotelDetailsDropDownTabList.element(by.css('.tabContent'));
    allDropdownDetailsTabPhotos: ElementArrayFinder = element.all(by.css('.photoGrid'));
    mapTabBtn: ElementFinder = this.hotelDetailsDropDownTabList.element(by.css("div[id*='-map']"));
    reviewsTabBtn: ElementFinder = this.hotelDetailsDropDownTabList.element(by.css("div[id*='-reviews']"));
    ratesTabBtn: ElementFinder = this.hotelDetailsDropDownTabList.element(by.css("div[id*='-rates']"));
    mapInMapTab: ElementFinder = this.activeTabContent.element(by.css("div[class='map']"));
    reviewsInReviewsTab: ElementFinder = this.activeTabContent.element(by.css('.topReviewGrid'));
    ratesInRatesTab: ElementFinder= this.activeTabContent.element(by.css('table'));

    getHotelsSearchResult(): ElementFinder {
        return this.hotelsSearchResult;
    }
    getAllHotelsResults(): ElementArrayFinder {
        return this.allSearchedHotels;
    }
    getFirstHotelName():ElementFinder {
        return this.allHotelNames.first();
    }
    getHotelDetailsDropdown(): ElementFinder {
        return this.allHotelDetailsDropdown.first();
    }
    getPhotosInDetailsTab(): ElementFinder {
        return this.allDropdownDetailsTabPhotos.first();
    }
    getMapTabBtn(): ElementFinder {
        return this.mapTabBtn;
    }
    getReviewsTabBtn(): ElementFinder {
        return this.reviewsTabBtn;
    }
    getRatesTabBtn(): ElementFinder {
        return this.ratesTabBtn;
    }
    getMapInMapTab(): ElementFinder {
        return this.mapInMapTab;
    }
    getReviewsInReviewsTab(): ElementFinder {
        return this.reviewsInReviewsTab;
    }
    getRatesInRatesTab(): ElementFinder {
        return this.ratesInRatesTab;
    }
}