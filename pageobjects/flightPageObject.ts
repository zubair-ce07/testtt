import { browser, by, element, ElementArrayFinder } from "protractor";
import BasePageObject from "./basePageObject";
import { convertMonthNameToShortName } from "../utils/common";

class FlightPageObject extends BasePageObject {
    private firstFlightDate: string;
    private secondFlightDate: string;
    private travelersText: string;

    setFlightDate(flightDate: string, legNo: number): void {
        const dateParts = flightDate.split(' ');
        const month = convertMonthNameToShortName(dateParts[0]);
        const convertedFlightDate = `${month} ${dateParts[1]}`;

        if (legNo === 0) {
            this.firstFlightDate = convertedFlightDate;
        }
        else {
            this.secondFlightDate = convertedFlightDate;
        }
    }

    getFirstFlightDate(): string {
        return this.firstFlightDate;
    }

    getSecondFlightDate(): string {
        return this.secondFlightDate;
    }

    setTravelersText(travelerText: string): void {
        this.travelersText = travelerText;
    }

    getTravelersText(): string {
        return this.travelersText;
    }

    openHomePage(): void {
        browser.get(this.currentSiteURL);
    };

    async openFlightsPage(): Promise<void> {
        const currentPageURL = await browser.getCurrentUrl();
        if (currentPageURL !== this.page.flightsPageURL) {
            const link = element(by.css(".js-vertical-flights")).element(by.linkText("Flights"));
            await link.click();
        }
    }

    async isFlightsPageDisplayed(): Promise<boolean> {
        const currentPageURL = await browser.getCurrentUrl();
        return currentPageURL === this.page.flightsPageURL;
    };

    async setFlightsToMultiCity(): Promise<void> {
        await this.page.selectFlightTypeMultiCity();
    }

    async getDisplayedFlightsCount(): Promise<number> {
        const multiCityFlightOptions = this.getMultiCityFlightOptions();
        return await multiCityFlightOptions.count();
    }

    getMultiCityFlightOptions(): any | ElementArrayFinder {
        const { multiCityLegsSelector } = this.page;
        return element.all(by.css(multiCityLegsSelector)).filter(element => element.isDisplayed());
    }

    async setFirstFlightDetail(origin: string, destination: string): Promise<void> {
        this.page.setLegNo(0);
        await this.setFlightDetail(origin, destination)
    }

    async setSecondFlightDetail(origin: string, destination: string): Promise<void> {
        this.page.setLegNo(1);
        await this.setFlightDetail(origin, destination)
    }

    async setFlightDetail(origin: string, destination: string): Promise<void> {
        const originInputField = await this.page.getOriginField();
        await originInputField.sendKeys(origin);
        await this.page.selectFirstOptionFromOriginsDropdown();

        const destinationInputField = await this.page.getDestinationField();
        await destinationInputField.sendKeys(destination);
        await this.page.selectFirstOptionFromDestinationDropdown();

        const flightDate = await this.page.setFlightDepartureDate();
        this.setFlightDate(flightDate, this.page.getLegNo());

        await this.page.setFlightTypeToBusiness();

        const travelerText = await this.page.getSelectedTravelerText();
        this.setTravelersText(travelerText);
    }

    async searchFlights(): Promise<void> {
        await this.page.clickSearchButton();
    }

    async isFlightSearchPageDisplayed(): Promise<boolean> {
        return await this.page.isFlightsSearchPageDisplayed()
    }
}

export default FlightPageObject;