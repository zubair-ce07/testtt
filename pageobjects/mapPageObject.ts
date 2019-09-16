import { protractor, browser, element, by, ElementArrayFinder, ElementFinder } from "protractor";
import { waitForElementPresence } from '../utils/common';

class mapPageObject {
    readonly hotelMarkerSelector: string = ".hotel-marker";
    private hotelMarkerId: string;

    setHotelMarkerId = (hotelMarkerId: string) => {
        this.hotelMarkerId = hotelMarkerId;
    };

    getHotelMarkerId = (): string => {
        return this.hotelMarkerId;
    };

    getAllHotelMarkers = (): ElementArrayFinder => {
        return element.all(by.css(this.hotelMarkerSelector));
    };

    getHotelInfo = async (): Promise<ElementFinder> => {
        const hotelMarker = await this.getSingleHotelMarker();
        await this.moveMouseOverHotelMarker(hotelMarker);
        await this.saveHoveredBoxDOMId(hotelMarker);
        return this.getHotelInfoHoverBox();
    };

    getSingleHotelMarker = async (): Promise<ElementFinder> => {
        const hotelMarkers = this.getAllHotelMarkers();
        const totalHotelMarkers = await hotelMarkers.count();
        console.log(`total hotel markers found: ${totalHotelMarkers}`);

        let selectedHotelMarker = null;
        for (let markerIndex = 0; markerIndex < totalHotelMarkers; markerIndex++) {
            const currentMarker = hotelMarkers.get(markerIndex);
            let top = await currentMarker.getCssValue('top');
            top = top.replace(/[a-z]/g, '');
            if (parseFloat(top) > 0) {
                selectedHotelMarker = currentMarker;
                break;
            }
        }

        return selectedHotelMarker;
    };

    moveMouseOverHotelMarker = async (hotelMarker): Promise<void> => {
        await browser.actions().mouseMove(hotelMarker).perform()
    };

    saveHoveredBoxDOMId = async (hotelMarker): Promise<void> => {
        let hoverBoxId = await hotelMarker.getAttribute("id");
        hoverBoxId = hoverBoxId.replace(/^\D+/g, '');
        this.setHotelMarkerId(hoverBoxId);
    };

    getHotelInfoHoverBox = (): ElementFinder => {
        const hoverBoxSelector = `summaryCard-${this.getHotelMarkerId()}`;
        return element(by.css(`[id=${hoverBoxSelector}]`));
    };

    getHotelCard = async (): Promise<ElementFinder> => {
        await this.getHotelInfoHoverBox().click();
        return this.getHotelCardImage();
    };

    getHotelCardImage = (): ElementFinder => {
        const hotelCardImage = element(by.css(`[id='${this.getHotelMarkerId()}-photo']`));
        waitForElementPresence(hotelCardImage, 1000, 'Timeout error! Hotel card image is taking too long to appear');
        return hotelCardImage;
    };

    openDealPage = async (): Promise<string> => {
        await this.clickViewDealButton();
        return await this.getDealPageURL();
    };

    clickViewDealButton = async (): Promise<void> => {
        const dealBtnSelector = `[id='${this.getHotelMarkerId()}-booking-bookButton']`;
        const viewDealBtn = element(by.css(dealBtnSelector));
        await viewDealBtn.click();
    };

    getDealPageURL = async (): Promise<string> => {
        await this.switchToNewTab();
        let EC = protractor.ExpectedConditions;
        browser.wait(EC.urlContains('kayak.com'), 5000);
        const dealPageUrl = await browser.getCurrentUrl();
        console.log('opened deal page url: ', dealPageUrl);
        return dealPageUrl;
    };

    switchToNewTab = async () => {
        const handles = await browser.getAllWindowHandles();
        await browser.switchTo().window(handles[1]);
    }
}

export default mapPageObject;