import {browser, $, element, by, protractor, promise, ElementFinder, ElementArrayFinder, ProtractorExpectedConditions, ExpectedConditions, Key} from 'protractor';
import { Helper } from './Helper';
var dragAndDrop = require('html-dnd').code;

export class KayakFlightsResultsPage {

    kayakHelper = new Helper();
    originAirportOfLegOne: ElementFinder = element(by.css("div[id$=origin0-airport-display]"));
    originAirportOfLegTwo: ElementFinder = element(by.css("div[id$=origin1-airport-display]"));
    legOneOfMultipleCities: ElementFinder = element(by.css("div[id$=multiCityLeg0]"));
    legTwoOfMultipleCities: ElementFinder = element(by.css("div[id$=multiCityLeg1]"));
    airportTimesFilter: ElementFinder = element(by.css("div[id$=-times]"));
    destinationAirportOfLegOne: ElementFinder = element(by.css("div[id$=destination0-airport-display]"));
    destinationAirportOfLegTwo: ElementFinder = element(by.css("div[id$=destination1-airport-display]"));
    cabinsSelectBoxOfLegOne: ElementFinder = element(by.css("div[id$=cabin_type0-display]"));
    cabinsSelectBoxOfLegTwo: ElementFinder = element(by.css("div[id$=cabin_type1-display]"));
    dateBoxOfLegOne: ElementFinder = this.legOneOfMultipleCities.element(by.css("div[id$=display-start]"));
    dateBoxOfLegTwo: ElementFinder = this.legTwoOfMultipleCities.element(by.css("div[id$=display-start]"));
    searchForm: ElementFinder = element(by.css("form[id$=searchform]"));
    travelerDropDown: ElementFinder = element(by.css("div[id$=travelers]"));
    adultTravelers: ElementFinder = element(by.css("input[id$=travelers-adults-input]"));
    seniorTravelers: ElementFinder = element(by.css("input[id$=travelers-seniors-input]"));
    youthTravelers: ElementFinder = element(by.css("input[id$=travelers-youth-input]"));
    childTravelers: ElementFinder = element(by.css("input[id$=travelers-child-input]"));
    seatInfantTravelers: ElementFinder = element(by.css("input[id$=travelers-seatInfant-input]"));
    lapInfantTravelers: ElementFinder = element(by.css("input[id$=travelers-lapInfant-input]"));
    timeSliderForZRH : ElementFinder = element(by.css("div[id$=times-takeoff-slider-1-sliderWidget-handle-0]"));
    timeSliderForFRA: ElementFinder = element(by.css("div[id$=times-takeoff-slider-0-sliderWidget-handle-0]"));
    viewDealButton: ElementFinder = element(by.css("div[id$=mb-best]"));
    clearAllButton: ElementFinder = element(by.css("button[id$=clearAll]"));
    timeSliderForZRHLabel: ElementFinder = element(by.css("div[id$=times-takeoff-label-1]"));
    timeSliderForFRALabel: ElementFinder = element(by.css("div[id$=times-takeoff-label-0]"));
    landingTab: ElementFinder = element(by.css("label[id$=times-Landing-label]"));
    takeOffTab: ElementFinder = element(by.css("label[id$=times-Take-off-label]"));
    landingSliderForZRH: ElementFinder = element(by.css("div[id$=times-landing-section-0]"));
    landingSliderForLON: ElementFinder = element(by.css("div[id$=times-landing-section-1]"));
    swissAirlinePrice: ElementFinder = element(by.css("button[id$='LX-price']"));
    loadingClass: ElementFinder = element(by.css("div[class*=no-spin]"));
    multipleCitiesForm: ElementFinder = element(by.css("form[name=mc-searchform]"));
    errorDialogBox: ElementFinder = element(by.css("div[class*=Common-Errors-ErrorDialog-Dialog]"));
    searchButton: ElementFinder = element(by.css("div[id$=submit-multi]"));
    firstErrorMessage: ElementFinder = element(by.css("ul[id$=-messages] li:nth-child(1)"));
    secondErrorMessage: ElementFinder = element(by.css("ul[id$=-messages] li:nth-child(2)"));
    thirdErrorMessage: ElementFinder = element(by.css("ul[id$=-messages] li:nth-child(3)"));
    takeOffSliderRange: ElementFinder = element(by.css("div[id$=times-takeoff-slider-1-rangeLabel]"));
    flightResults: ElementArrayFinder = element.all(by.css(".Flights-Results-FlightResultItem"));
    erorDialogCloseButton: ElementFinder = element(by.css("button[class*=errorDialogCloseButton]"))

    async getOriginAirportOfLegOne(): Promise<string> {
        return await this.originAirportOfLegOne.getText();
        browser.params
    }

    async multipleCitiesFormDisplayed(): Promise<boolean> {
        return await this.multipleCitiesForm.isDisplayed();
    }

    async getOriginAirportOfLegTwo(): Promise<string> {
        return await this.originAirportOfLegTwo.getText();
    }

    async getDestinationAirportOfLegOne(): Promise<string> {
        return await this.destinationAirportOfLegOne.getText();
    }

    async getDestinationAirportOfLegTwo(): Promise<string> {
        return await this.destinationAirportOfLegTwo.getText();
    }

    async airportTimesFilterDisplayed(): Promise<boolean> {
        await browser.wait(ExpectedConditions.visibilityOf(this.airportTimesFilter), 20000);
        return await this.airportTimesFilter.isDisplayed();
    }

    async getSelectedDateOfLegOne(): Promise<string> {
        const selectedDateOfLegOne = await this.dateBoxOfLegOne.getText();
        return await selectedDateOfLegOne.trim();
    }

    async getSelectedDateOfLegTwo(): Promise<string> {
        const selectedDateOfLegTwo = await this.dateBoxOfLegTwo.getText();
        return await selectedDateOfLegTwo.trim();
    }

    async getSelectedCabinOfLegOne(): Promise<string> {
        return await this.cabinsSelectBoxOfLegOne.getText();
    }

    async getSelectedCabinOfLegTwo(): Promise<string> {
        return await this.cabinsSelectBoxOfLegTwo.getText();
    }

    async clickSearchForm(): Promise<void> {
        await this.searchForm.click();
    }

    async clickTravelers(): Promise<void> {
        await this.travelerDropDown.click();
    }
    
    async defaultTravelersSelected(): Promise<boolean> {
        const adultTravelers = await this.adultTravelers.getAttribute("value");
        const seniorTravelers = await this.seniorTravelers.getAttribute("value");
        const youthTravelers = await this.youthTravelers.getAttribute("value");
        const childTravelers = await this.childTravelers.getAttribute("value");
        const seatInfantTravelers = await this.seatInfantTravelers.getAttribute("value");
        const lapInfantTravelers = await this.lapInfantTravelers.getAttribute("value");
        return (adultTravelers === "1" && seniorTravelers === "0" && youthTravelers === "0"
        && childTravelers === "0" && seatInfantTravelers === "0" && lapInfantTravelers === "0");
    }

    async changeTimeSliderForZRH(): Promise<void> {
        await browser.actions().dragAndDrop(this.timeSliderForZRH, {x: 1000, y: 0}).mouseUp().perform();
        await browser.sleep(8000);
    }

    async timeSliderForZRHChanged(): Promise<boolean> {
        let takeOffRange: string = await this.takeOffSliderRange.getText();
        return await takeOffRange.indexOf("6:00") === -1;
    }


    async timeInRange(value: Array<string>, range: Array<string>): Promise<boolean> {
        return await value[0] >= range[0] && value[1] <= range[1];
    }

    async clickViewDealButton(): Promise<void> {
        await this.swissAirlinePrice.click();
		await browser.wait(ExpectedConditions.invisibilityOf(this.loadingClass), 10000);
        await this.viewDealButton.click();
    }

    async switchTab(): Promise<void> {
		await browser.getAllWindowHandles().then((handles) => {
			browser.driver.switchTo().window(handles[0]);
		});
    }
    
    async twoTakeOffSlidersDisplayed(): Promise<boolean> {
        return (await this.timeSliderForFRA.isDisplayed() && await this.timeSliderForZRH.isDisplayed());
    }

    async getSecondSliderLabel(): Promise<string> {
        let labelOfFRASlider = await this.timeSliderForZRHLabel.getText();
        return await labelOfFRASlider.replace(/\s\s+/g, "");
    }

    async getFirstSliderLabel(): Promise<string> {
        let labelOfFRASlider = await this.timeSliderForFRALabel.getText();
        return await labelOfFRASlider.replace(/\s\s+/g, "");
    }

    async clickLandingTabInTimesFilter(): Promise<void> {
        await this.landingTab.click();
    }

    async clickTakeOffTimesFilter(): Promise<void> {
        await this.takeOffTab.click();
    }

    async twoLandingSlidersDisplayed(): Promise<boolean> {
        return (await this.landingSliderForLON.isDisplayed() && await this.landingSliderForZRH.isDisplayed());
    }

    async clickClearAllButton(): Promise<void> {
        await this.clearAllButton.click();
    }

    async clearLegOneOriginAirport(): Promise<boolean> {
        return await this.getOriginAirportOfLegOne() === "From";
    }

    async clearLegTwoOriginAirport(): Promise<boolean> {
        return await this.getOriginAirportOfLegTwo() === "From";
    }

    async clearLegOneDestinationAirport(): Promise<boolean> {
        return await this.getDestinationAirportOfLegOne() === "To";
    }

    async clearLegTwoDestinationAirport(): Promise<boolean> {
        return await this.getDestinationAirportOfLegTwo() === "To";
    }

    async clearLegOneDepartureDate(): Promise<boolean> {
        return await this.getSelectedDateOfLegOne() === "Depart";
    }

    async clearLegTwoDepartureDate(): Promise<boolean> {
        return await this.getSelectedDateOfLegTwo() === "Depart";
    }

    async notClearLegOneCabinClass(): Promise<boolean> {
        return await this.getSelectedCabinOfLegOne() === "Business";
    }

    async notClearLegTwoCabinClass(): Promise<boolean> {
        return await this.getSelectedCabinOfLegTwo() === "Business";
    }

    async notClearSelectedTravelers(): Promise<boolean> {
       return this.defaultTravelersSelected();
    }

    async clickSearchButton(): Promise<void> {
        await browser.wait(ExpectedConditions.visibilityOf(this.searchButton), 5000);
        await this.searchButton.click();
    }

    async errorDialogBoxDisplayed(): Promise<boolean> {
        await browser.wait(ExpectedConditions.visibilityOf(this.errorDialogBox), 5000);
        return await this.errorDialogBox.isDisplayed();
    }

    async getFirstErrorMessage(): Promise<string> {
        return await this.firstErrorMessage.getText();
    }

    async getSecondErrorMessage(): Promise<string> {
        return await this.secondErrorMessage.getText();
    }

    async getThirdErrorMessage(): Promise<string> {
        return await this.thirdErrorMessage.getText();
    }

    async clickErrorDialogOkButton(): Promise<void> {
        await this.erorDialogCloseButton.click();
    }

    async closeErrorDialogBox(): Promise<boolean> {
        return !(await this.errorDialogBoxDisplayed());
    }

    async resultsContainNewTimeRangeForSecondLeg(): Promise<boolean> {
        await browser.wait(ExpectedConditions.invisibilityOf(this.loadingClass), 30000);
        let takeOffLabel: string = await this.takeOffSliderRange.getText();
        let takeOffRange: Array<string> = takeOffLabel.trim().match(/(\d\d?:\d\d)/g);
		return this.flightResults.then(async function(results) {
			for(let result of results) {
				let timeInResults: string = await result.element(by.css("div[id$=info-leg-1] .section.times")).getText();
                if(!(await this.timeInRange(timeInResults.trim().match(/(\d\d?:\d\d)/g), takeOffRange))) {
                    return false;
                }
			}
			return true;
		});
    }
}