import HotelPageObject from './../pageobjects/hotelPageObject';
import HotelSearchResultPageObject from './../pageobjects/hotelSearchResultPageObject';
import MapPageObject from './../pageobjects/mapPageObject';

describe('Hotels Sanity -', () => {
    const hotelPage: HotelPageObject = new HotelPageObject();
    const hotelSearchResultPage: HotelSearchResultPageObject = new HotelSearchResultPageObject();
    const mapPage: MapPageObject = new MapPageObject();
    enum TabsName {
        Map = "map",
        Review = "review",
        Rate = "rates"
    }
    enum PageName {
        Hotels = "Hotels Page -",
        HotelsSearchResult = "Hotels Search Result Page -",
        Map = "Map Page -",
        Deal = "Deal Page -"
    }

    it(`${PageName.Hotels} Should open hotels front page`, () => {
        hotelPage.openHomePage();
        hotelPage.openHotelsPage();
        expect(<any>hotelPage.isHotelPageDisplayed()).toBe(true);
    });

    it(`${PageName.Hotels} Should display the origin field`, () => {
        expect(<any>hotelPage.getOriginField().isDisplayed()).toBe(true);
    });

    it(`${PageName.Hotels} Should display the start date field`, () => {
        expect(<any>hotelPage.getTravelStartDate().isDisplayed()).toBe(true);
    });

    it(`${PageName.Hotels} Should display the end date field`, () => {
        expect(<any>hotelPage.getTravelEndDate().isDisplayed()).toBe(true);
    });

    it(`${PageName.Hotels} Should display ‘1 room, 2 guests’ in guests field`, () => {
        expect(<any>hotelPage.getGuestField().getText()).toEqual(hotelPage.guestFieldText);
    });

    it(`${PageName.HotelsSearchResult} Should load hotels results page`, async () => {
        await hotelPage.setOriginToBCN();
        await hotelPage.searchHotels();
        hotelSearchResultPage.waitForSearchCompletion();
        expect(<any>hotelSearchResultPage.getHotelSearchResultPage().isDisplayed()).toBe(true);
    });

    it(`${PageName.HotelsSearchResult} Should display at least 5 hotel results`, async () => {
        const searchResult = hotelSearchResultPage.getHotelSearchResult();
        const hotelsCount = await searchResult.count();
        console.log(`hotels count ${hotelsCount}`);
        expect(hotelsCount).toBeGreaterThan(4);
    });

    it(`${PageName.HotelsSearchResult} Should display hotel details section`, async () => {
        const hostelDetail = await hotelSearchResultPage.openSingleHotelDetail();
        expect(hostelDetail.isDisplayed()).toBe(true);
    });

    it(`${PageName.HotelsSearchResult} Should display hotel images in ‘Details’ section"`, async () => {
        const photosCount = await hotelSearchResultPage.getFirstHotelPhotos().count();
        expect(photosCount).toBeGreaterThan(0);
        console.log(`hotel photos count: ${photosCount}`);
    });

    it(`${PageName.HotelsSearchResult} Should display map in ‘Map’ section`, async () => {
        const mapContent = await hotelSearchResultPage.openTab(TabsName.Map);
        expect(mapContent.isDisplayed()).toBe(true);
    });

    it(`${PageName.HotelsSearchResult} Should display reviews in ‘Reviews’ section`, async () => {
        const reviewContent = await hotelSearchResultPage.openTab(TabsName.Review);
        expect(reviewContent.isDisplayed()).toBe(true);
    });

    it(`${PageName.HotelsSearchResult} Should display rates in ‘Rates’ section`, async () => {
        const ratesContent = await hotelSearchResultPage.openTab(TabsName.Rate);
        expect(ratesContent.isDisplayed()).toBe(true);
    });

    it(`${PageName.HotelsSearchResult} Should display map view`, async () => {
        const mapContent = await hotelSearchResultPage.getGoToMap();
        expect(mapContent.isDisplayed()).toBe(true);
    });

    it(`${PageName.Map} Should display hotel info`, async () => {
        const hotelInfo = await mapPage.getHotelInfo();
        expect(hotelInfo.isDisplayed()).toBe(true);
    });

    it(`${PageName.Map} Should display hotel card on the left side`, async () => {
        const hotelCardImage = await mapPage.getHotelCard();
        expect(hotelCardImage.isDisplayed()).toBe(true);
    });

    it(`${PageName.Deal} Should open provider page in new tab`, async () => {
        const dealPageURL = await mapPage.openDealPage();
        expect(dealPageURL).toContain("kayak.com");
    });
});