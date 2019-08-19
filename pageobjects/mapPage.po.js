import { waitForElementPresence } from './../utils/common';

let mapPage = function () {

    this.hotelMarkerSelector = ".hotel-marker";

    this.setHotelMarkerId = (hotelMarkerId) => {
        this.hotelMarkerId = hotelMarkerId;
    };

    this.getHotelMarkerId = () => {
        return this.hotelMarkerId;
    };

    this.getAllHotelMarkers = () => {
        return element.all(by.css(this.hotelMarkerSelector));
    };

    this.getHotelInfo = async () => {
        const hotelMarker = await this.getSingleHotelMarker();
        await this.moveMouseOverHotelMarker(hotelMarker);
        await this.saveHoveredBoxDOMId(hotelMarker);
        return this.getHotelInfoHoverBox();
    };

    this.getSingleHotelMarker = async () => {
        const hotelMarkers = this.getAllHotelMarkers();
        const totalHotelMarkers = await hotelMarkers.count();
        console.log(`total hotel markers found: ${totalHotelMarkers}`);

        let selectedHotelMarker = null;
        for (let markerIndex = 0; markerIndex < totalHotelMarkers; markerIndex++) {
            const currentMarker = hotelMarkers.get(markerIndex);
            let top = await currentMarker.getCssValue('top');
            top = top.replace(/\D/g, '');
            if (top > 0) {
                selectedHotelMarker = currentMarker;
                break;
            }
        }

        return selectedHotelMarker;
    };

    this.moveMouseOverHotelMarker = async (hotelMarker) => {
        await browser.actions().mouseMove(hotelMarker).perform()
    };

    this.saveHoveredBoxDOMId = async (hotelMarker) => {
        let hoverBoxId = await hotelMarker.getAttribute("id");
        hoverBoxId = hoverBoxId.replace(/^\D+/g, '');
        this.setHotelMarkerId(hoverBoxId);
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
        await this.switchToNewTab();
        let EC = protractor.ExpectedConditions;
        browser.wait(EC.urlContains('kayak.com'), 5000);
        const dealPageUrl = await browser.getCurrentUrl();
        console.log('opened deal page url: ', dealPageUrl);
        return dealPageUrl;
    };

    this.switchToNewTab = async () => {
        const handles = await browser.getAllWindowHandles();
        await browser.switchTo().window(handles[1]);
    }
};

export default mapPage;