import { waitForElementPresence } from './../utils/common';

let mapPage = function () {
    this.getMapPageInfo = () => {
        return {
            hotelMarkerSelector: ".hotel-marker",
        }
    };

    this.setHotelMarkerId = (hotelMarkerId) => {
        this.hotelMarkerId = hotelMarkerId;
    };

    this.getHotelMarkerId = () => {
        return this.hotelMarkerId;
    };

    this.getAllHotelMarkers = () => {
        return element.all(by.css(this.getMapPageInfo().hotelMarkerSelector));
    };

    this.getHotelInfo = async () => {
        const hotelMarker = await this.getSingleHotelMarker();
        await this.moveMouseOverHotelMarker(hotelMarker);
        const hotelMarkerId = await this.getHotelInfoHoverBoxIdInDOM(hotelMarker);
        this.setHotelMarkerId(hotelMarkerId);
        return this.getHotelInfoHoverBox();
    };

    this.getSingleHotelMarker = async () => {
        const hotelMarkers = this.getAllHotelMarkers();
        const totalHotelMarkers = await hotelMarkers.count();
        console.log(`total hotel markers found: ${totalHotelMarkers}`);

        let hotelMarker = null;
        for (let markerIndex = 0; markerIndex < totalHotelMarkers; markerIndex++) {
            const selectedMarker = hotelMarkers.get(markerIndex);
            let top = await selectedMarker.getCssValue('top');
            top = top.replace(/\D/g, '');
            if (top > 0) {
                hotelMarker = selectedMarker;
                break;
            }
        }

        return hotelMarker;
    };

    this.moveMouseOverHotelMarker = async (hotelMarker) => {
        await browser.actions().mouseMove(hotelMarker).perform()
    };

    this.getHotelInfoHoverBoxIdInDOM = async (hotelMarker) => {
        let hoverBoxId = await hotelMarker.getAttribute("id");
        hoverBoxId = hoverBoxId.replace(/^\D+/g, '');
        return hoverBoxId;
    };

    this.getHotelInfoHoverBox = () => {
        const hoverBoxSelector = `summaryCard-${this.getHotelMarkerId()}`;
        return element(by.css(`[id=${hoverBoxSelector}]`));
    };

    this.getHotelCard = async () => {
        await this.getHotelInfoHoverBox().click();
        return this.getHotelCardImage();
    };

    this.getHotelCardImage = () => {
        const hotelCardImage = element(by.css(`[id='${this.getHotelMarkerId()}-photo']`));
        waitForElementPresence(hotelCardImage, 1000, 'Timeout error! Hotel card image is taking too long to appear');
        return hotelCardImage;
    };

    this.openDealPage = async () => {
        await this.clickViewDealButton();
        return await this.getDealPageURL();
    };

    this.clickViewDealButton = async () => {
        const dealBtnSelector = `[id='${this.getHotelMarkerId()}-booking-bookButton']`;
        const viewDealBtn = element(by.css(dealBtnSelector));
        await viewDealBtn.click();
    };

    this.getDealPageURL = async () => {
        const handles = await browser.getAllWindowHandles();
        await browser.switchTo().window(handles[1]);
        let EC = protractor.ExpectedConditions;
        browser.wait(EC.urlContains('kayak.com'), 5000);
        const dealPageUrl = await browser.getCurrentUrl();
        console.log('opened deal page url: ', dealPageUrl);
        return dealPageUrl;
    };
};

export default mapPage;