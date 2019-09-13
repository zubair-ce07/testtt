import {by, element, ElementFinder} from "protractor";

export default class MapPageElements {
    showMapBtn: ElementFinder = element(by.css('.filterList')).element(by.css('.Common-Results-MapToggle'));
    mainMap: ElementFinder = element(by.css('.Hotels-Results-HotelRightRailMap'));
    horizontalFilters: ElementFinder = element(by.css('.horizontal-filters-wrapper'));
    hotelMarker: ElementFinder = element(by.css('.hotel-marker'));

    getShowMapBtn():ElementFinder {
        return this.showMapBtn;
    }
    getMainMap(): ElementFinder {
        return this.mainMap;
    }
    getHorizontalFilters(): ElementFinder {
        return this.horizontalFilters;
    }
    getHotelMarker(): ElementFinder {
        return this.hotelMarker;
    }
    getHotelInfoHoverCard(hotelMarkerID: string): ElementFinder {
        return element(by.css('#summaryCard-'+hotelMarkerID))
    }
    getHotelCard(hotelMarkerID: string): ElementFinder {
        const hotelCardID = hotelMarkerID+"-detailsWrapper";
        return element(by.id(hotelCardID));
    }
    getViewDealBtn(hotelMarkerID: string): ElementFinder {
        const viewDetailsBtnID = hotelMarkerID+"-booking-bookButton";
        return element(by.id(viewDetailsBtnID));
    }
    getBookingProvider(hotelMarkerID: string): ElementFinder {
        const bookingProviderID = hotelMarkerID + "-booking-provider";
        return element(by.id(bookingProviderID)).all(by.css('div')).get(2);
    }
}