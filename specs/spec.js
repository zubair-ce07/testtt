import hotelPageObject from './../pageobjects/hotelPage.po';
import hotelSearchResultPageObject from './../pageobjects/hotelSearchResultPage.po';
import mapPageObject from './../pageobjects/mapPage.po';

describe('KAYAK App', () => {
    let hotelPage = new hotelPageObject();
    let hotelSearchResultPage = new hotelSearchResultPageObject();
    let mapPage = new mapPageObject();
    let hotelInfoHoverBox = null;
    let hotelInfoHoverBoxIdInDOM = null;

    it("Should display the origin field", () => {
        hotelPage.openHomePage();
        hotelPage.clickHotelsPage();
        expect(hotelPage.isHotelPageDisplayed()).toBe(true);
        expect(hotelPage.getOriginField().isDisplayed()).toBe(true);
    });

    it("Should display the start date field", () => {
        const {startDate } = hotelPage.getDateFields();
        expect(startDate.isDisplayed()).toBe(true);
    });

    it("Should display the end date field", () => {
        const {endDate } = hotelPage.getDateFields();
        expect(endDate.isDisplayed()).toBe(true);
    });

    it("Should display ‘1 room, 2 guests’ in guests field", () => {
        expect(hotelPage.getGuestField().getText()).toEqual(hotelPage.getHotelPageInfo().guestFieldText);
    });

    it("Should load hotels results page", async () => {
        await hotelPage.setTextInOriginField('BCN');
        hotelSearchResultPage.waitForOriginsListPresence();
        await hotelPage.selectFirstOriginFromOriginsList();
    });

    it("Should display at least 5 hotel results", async () => {
        await hotelSearchResultPage.clickSearchHotelsButton();
        hotelSearchResultPage.waitForSearchCompletion();
        const searchResult = hotelSearchResultPage.getHotelSearchResult();
        const hotelsCount = await searchResult.count();
        console.log(`hotels count ${hotelsCount}`);
        expect(hotelsCount).toBeGreaterThan(4);
    });

    it("Should display hotel details section", async () => {
        await hotelSearchResultPage.clickFirstHotelTitle();
        const hostelDetail = hotelSearchResultPage.getFirstHotelDetail();
        expect(hostelDetail.isDisplayed()).toBe(true);
    });

    it("Should display hotel images in ‘Details’ section", async() => {
        const photosCount = await hotelSearchResultPage.getFirstHotelPhotos().count();
        expect(photosCount).toBeGreaterThan(0);
        console.log(`hotel photos count: ${photosCount}`);
    });

    it("Should display map in ‘Map’ section", async() => {
        const tabName = 'map';
        await hotelSearchResultPage.clickSelectedHotelTab(tabName);
        const mapContent = hotelSearchResultPage.getTabContent(tabName);
        //const mapCount = await mapContent.count();
        expect(mapContent.isDisplayed()).toBe(true);
    });

    it("Should display reviews in ‘Reviews’ section", async() => {
        const tabName = 'review';
        await hotelSearchResultPage.clickSelectedHotelTab(tabName);
        const reviewContent = hotelSearchResultPage.getTabContent(tabName);
        expect(reviewContent.isDisplayed()).toBe(true);
    });

    it("Should display rates in ‘Rates’ section", async() => {
        const tabName = 'rates';
        await hotelSearchResultPage.clickSelectedHotelTab(tabName);
        const ratesContent = hotelSearchResultPage.getTabContent(tabName);
        expect(ratesContent.isDisplayed()).toBe(true);
    });

    it("Should display map view", async() => {
        await hotelSearchResultPage.clickGoToMap();
        const mapContent = hotelSearchResultPage.getMap();
        expect(mapContent.isDisplayed()).toBe(true);
    });

    it("Should display hotel info", async () => {
        const hotelMarker = await mapPage.getSingleHotelMarker();
        await mapPage.moveMouseOverHotelMarker(hotelMarker);
        hotelInfoHoverBoxIdInDOM = await mapPage.getHotelInfoHoverBoxIdInDOM(hotelMarker);
        hotelInfoHoverBox = mapPage.getHotelInfoHoverBox(hotelInfoHoverBoxIdInDOM);
        expect(hotelInfoHoverBox.isDisplayed()).toBe(true);
    });
    
    it("Should display hotel card on the left side", async () => {
        await hotelInfoHoverBox.click();
        const hotelCardImage = mapPage.getHotelCardImage(hotelInfoHoverBoxIdInDOM);
        expect(hotelCardImage.isDisplayed()).toBe(true);
    });

    it("Should open provider page in new tab", async () => {
        await mapPage.clickViewDealButton(hotelInfoHoverBoxIdInDOM);
        const dealPageURL = await mapPage.getDealPageURL();
        expect(dealPageURL && dealPageURL.length > 0).toBe(true);
    });
});