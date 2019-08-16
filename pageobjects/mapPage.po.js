import * as utils from './../utils/common';

let mapPage = function() {
    this.getAllHotelMarkers = () => {
        return element.all(by.css('.hotel-marker'));
    };

    this.getSingleHotelMarker = async () => {
        //return hotelMarkers.get(index);
        const hotelMarkers = this.getAllHotelMarkers();
        const totalHotelMarkers = await hotelMarkers.count();
        console.log(`total hotel markers found: ${totalHotelMarkers}`);

        let hotelMarker = null;
        for(let markerIndex = 0; markerIndex < totalHotelMarkers; markerIndex++) {
            const selectedMarker = hotelMarkers.get(markerIndex);
            let top = await selectedMarker.getCssValue('top');
            top = top.replace(/\D/g,'');
            if(top > 0) {
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

    this.getHotelInfoHoverBox = (hoverBoxId) => {
        const hoverBoxSelector = `summaryCard-${hoverBoxId}`;
        return element(by.css(`div[id=${hoverBoxSelector}]`));
    };

    this.getHotelCardImage = (hotelInfoHoverBoxId) => {
        const hotelCardImage = element(by.css(`div[id='${hotelInfoHoverBoxId}-photo']`));
        utils.waitForElementPresence(hotelCardImage, 1000, 'Timeout error! Hotel card image is taking too long to appear');
        return hotelCardImage;
    };

    this.clickViewDealButton = async (hotelInfoHoverBoxId) => {
        const dealBtnSelector = `button[id='${hotelInfoHoverBoxId}-booking-bookButton']`;
        const viewDealBtn = element(by.css(dealBtnSelector));
        await viewDealBtn.click();
        browser.sleep(5000);
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