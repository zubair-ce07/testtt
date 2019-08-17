import hotelPageObject from './../pageobjects/hotelPage.po';
import hotelSearchResultPageObject from './../pageobjects/hotelSearchResultPage.po';
import mapPageObject from './../pageobjects/mapPage.po';

describe('Hotels Sanity - Front Page - Search Result Page - Map Page - Hotel Deals Page', () => {
    const hotelPage = new hotelPageObject();
    const hotelSearchResultPage = new hotelSearchResultPageObject();
    const mapPage = new mapPageObject();
    const tabsName = {
        map: "map",
        review: "review",
        rate: "rates"
    };

    it(" Should open hotels front page", () => {
        hotelPage.openHomePage();
        hotelPage.openHotelsPage();
        expect(hotelPage.isHotelPageDisplayed()).toBe(true);
    });

    it("Should display the origin field", () => {
        expect(hotelPage.getOriginField().isDisplayed()).toBe(true);
    });

    it("Should display the start date field", () => {
        expect(hotelPage.getTravelStartDate().isDisplayed()).toBe(true);
    });

    it("Should display the end date field", () => {
        expect(hotelPage.getTravelEndDate().isDisplayed()).toBe(true);
    });

    it("Should display ‘1 room, 2 guests’ in guests field", () => {
        expect(hotelPage.getGuestField().getText()).toEqual(hotelPage.getHotelPageInfo().guestFieldText);
    });

    it("Should load hotels results page", async () => {
        await hotelPage.setOriginToBCN();
        await hotelPage.searchHotels();
        hotelSearchResultPage.waitForSearchCompletion();
        expect(hotelSearchResultPage.getHotelSearchResultPage().isDisplayed()).toBe(true);
    });

    it("Should display at least 5 hotel results", async () => {
        const searchResult = hotelSearchResultPage.getHotelSearchResult();
        const hotelsCount = await searchResult.count();
        console.log(`hotels count ${hotelsCount}`);
        expect(hotelsCount).toBeGreaterThan(4);
    });

    it("Should display hotel details section", async () => {
        const hostelDetail = await hotelSearchResultPage.openSingleHotelDetail();
        expect(hostelDetail.isDisplayed()).toBe(true);
    });

    it("Should display hotel images in ‘Details’ section", async () => {
        const photosCount = await hotelSearchResultPage.getFirstHotelPhotos().count();
        expect(photosCount).toBeGreaterThan(0);
        console.log(`hotel photos count: ${photosCount}`);
    });

    it("Should display map in ‘Map’ section", async () => {
        const mapContent = await hotelSearchResultPage.openTab(tabsName.map);
        expect(mapContent.isDisplayed()).toBe(true);
    });

    it("Should display reviews in ‘Reviews’ section", async () => {
        const reviewContent = await hotelSearchResultPage.openTab(tabsName.review);
        expect(reviewContent.isDisplayed()).toBe(true);
    });

    it("Should display rates in ‘Rates’ section", async () => {
        const ratesContent = await hotelSearchResultPage.openTab(tabsName.rate);
        expect(ratesContent.isDisplayed()).toBe(true);
    });

    it("Should display map view", async () => {
        const mapContent = await hotelSearchResultPage.getGoToMap();
        expect(mapContent.isDisplayed()).toBe(true);
    });

    it("Should display hotel info", async () => {
        const hotelInfo = await mapPage.getHotelInfo();
        expect(hotelInfo.isDisplayed()).toBe(true);
    });

    it("Should display hotel card on the left side", async () => {
        const hotelCardImage = await mapPage.getHotelCard();
        expect(hotelCardImage.isDisplayed()).toBe(true);
    });

    it("Should open provider page in new tab", async () => {
        const dealPageURL = await mapPage.openDealPage();
        expect(dealPageURL).toContain("kayak.com");
    });
});