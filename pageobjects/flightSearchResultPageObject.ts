import { browser, by, element, ElementArrayFinder, ElementFinder, protractor } from "protractor";
import BasePageObject from "./basePageObject";
import { convertDateInFormatMonthInNumberSlashDayInNumber, convertTimeToMinutes } from "../utils/common";

class FlightSearchResultPageObject extends BasePageObject {
    async getAppliedAirportFilter(): Promise<string> {
        const airportFilterField = element(by.css("[id$=-multiCityDisplay]"));
        return await airportFilterField.getText();
    }

    async getAppliedTravelerFilter(): Promise<string> {
        const travelerFilterField = this.page.getAppliedTravelerFilterField();
        return await travelerFilterField.getText();
    }

    async getAppliedDateFilter(): Promise<string> {
        const dateFilterField = element(by.css("[id$=-multiCityDates]"));
        return await dateFilterField.getText();
    }

    async doesFirstAppliedDateFilterMatchFlightDate(departureDate: string): Promise<boolean> {
        const appliedDateFilter = await this.getAppliedDateFilter();
        return appliedDateFilter.indexOf(departureDate) !== -1;
    }

    async getAppliedCabinClass(): Promise<string> {
        return await browser.executeScript('return document.querySelector("[id$=-cabin-content]").querySelector(".label").innerText');
    }

    async getCountOfDisplayedTakeOffSliders(): Promise<number> {
        const sliders = this.getTakeOffSliders();
        return this.getSliders(sliders);
    }

    getTakeOffSliders(): ElementArrayFinder {
        return element(by.css("[id$=-times-timesSection]")).all(by.css("[id$=-times-takeoff]")).first().all(by.css(".js-legSection.timesFilterSection"));
    }

    async getCountOfDisplayedLandingSliders(): Promise<number> {
        await this.selectLandingTab();
        const sliders = this.getLandingSliders();
        return await this.getSliders(sliders);
    }

    async selectTakeOffTab(): Promise<void> {
        const selectedTab = element(by.css(".takeoffLandingTabs")).element(by.css("[id$=-times-Take-off-label]"));
        ;
        await selectedTab.click();
    }

    async selectLandingTab(): Promise<void> {
        const selectedTab = element(by.css(".takeoffLandingTabs")).element(by.css("[id$=-times-Landing-label]"));
        await selectedTab.click();
    }

    getLandingSliders(): ElementArrayFinder {
        return element(by.css("[id$=-times-timesSection]")).all(by.css("[id$=-times-landing]")).first().all(by.css(".js-legSection.timesFilterSection"));
    }

    async getSliders(sliders): Promise<number> {
        const totalSliders = await sliders.count();
        let slidersDisplayed = 0;
        if (totalSliders >= 2) {
            if (await sliders.get(0).isDisplayed()) {
                slidersDisplayed++;
            }

            if (await sliders.get(1).isDisplayed()) {
                slidersDisplayed++;
            }
            return slidersDisplayed;
        }
        return totalSliders;
    }

    async getSliderTakeOffOrigin(legNo: number): Promise<string> {
        const slider = element(by.css("[id$=-times-timesSection]")).element(by.css(`[id$=-times-takeoff-label-${legNo}]`));
        return await slider.getText();
    }

    async getSliderLandingDestination(legNo: number): Promise<string> {
        const slider = element(by.css("[id$=-times-timesSection]")).element(by.css(`[id$=-times-landing-label-${legNo}]`));
        return await slider.getText();
    }

    async slideTakeOffSliderForZRH(): Promise<number> {
        this.selectTakeOffTab();
        const takeOffStartTime = await this.slideSecondTakeOffSlider();
        return convertTimeToMinutes(takeOffStartTime);
    };

    async slideSecondTakeOffSlider(): Promise<string> {
        const slider = element(by.css("[id$=-times-takeoff-slider-1-sliderWidget-handle-0]"));
        await browser.executeScript("arguments[0].style.left='20%'", slider);

        let EC = protractor.ExpectedConditions;
        await browser.wait(EC.invisibilityOf(element(by.css(".no-spin.loading"))), 20000, "Timeout Error! flights search loading spinner is taking too long to hide");

        const takeoffTimeLabel = element(by.css("[id$=-times-takeoff-slider-1-rangeLabel]")).element(by.css(".min"));
        const takeOffStartDayAndTime = await takeoffTimeLabel.getText();
        return takeOffStartDayAndTime.substr(takeOffStartDayAndTime.indexOf(" ") + 1).trim();
    }

    async getTotalSearchedFlightsCount(): Promise<number> {
        return await this.page.getSearchedFlightsCount();
    }

    async getTakeOffTimeForFlightZRH(flightResultNo: number): Promise<number> {
        const flightTakeOffTime = await this.page.getSearchedFlightTakeOffTime(flightResultNo);
        return convertTimeToMinutes(flightTakeOffTime);
    };

    async openDealPage(): Promise<number> {
        await this.clickFirstFlightViewDealButton();
        const handles = await browser.getAllWindowHandles();
        await browser.switchTo().window(handles[0]);
        return handles.length;
    }

    async clickFirstFlightViewDealButton(): Promise<void> {
        const firstFlight = element.all(by.css("[id$=-mb-featuredFare]")).get(0).element(by.css(".booking-link"));
        await firstFlight.click();

        let EC = protractor.ExpectedConditions;
        browser.wait(EC.urlContains('/book/flight'), 10000);
    }

    async searchFlightAgain(): Promise<void> {
        const searchButton = element(by.css(".Flights-Search-FlightInlineSearchForm")).element(by.css("[id$=-submit]"));
        await searchButton.click();
    }

    async isMultiFormDisplayed(): Promise<boolean> {
        const multiCityForm = element(by.name("mc-searchform"));
        return await multiCityForm.isDisplayed();
    }

    async getMultiCityFormFirstAirportsFilter(): Promise<{ flightOrigin: string, flightDestination: string }> {
        this.page.setLegNo(0);
        return await this.page.getMultiCityFormOriginAndDestination();
    }

    async getMultiCityFormSecondAirportsFilter(): Promise<{ flightOrigin: string, flightDestination: string }> {
        this.page.setLegNo(1);
        return await this.page.getMultiCityFormOriginAndDestination();
    }

    async getMultiCityFormFirstCabinClassFilter(): Promise<string> {
        this.page.setLegNo(0);
        return await this.page.getMultiCityFormCabinClass();
    }

    async getMultiCityFormSecondCabinClassFilter(): Promise<string> {
        this.page.setLegNo(1);
        return await this.page.getMultiCityFormCabinClass();
    }

    async getMultiCityFormTravelerFilter(): Promise<string> {
        return await this.page.getMultiCityFormTraveler();
    }

    async getMultiCityFormFirstFlightDateFilter(): Promise<string> {
        this.page.setLegNo(0);
        return await this.page.getMultiCityFormDate();
    }

    async getMultiCityFormSecondFlightDateFilter(): Promise<string> {
        this.page.setLegNo(1);
        return await this.page.getMultiCityFormDate();
    }

    async isMCFormFilterFirstDateMatchAppliedFilterDate(flightDate): Promise<boolean> {
        this.page.setLegNo(0);
        return await this.isMCFormDateMatchedFlightDate(flightDate);
    }

    async isMCFormFilterSecondDateMatchAppliedFilterDate(flightDate): Promise<boolean> {
        this.page.setLegNo(1);
        return await this.isMCFormDateMatchedFlightDate(flightDate);
    }

    async isMCFormDateMatchedFlightDate(flightDate): Promise<boolean> {
        const flightFilterDate = convertDateInFormatMonthInNumberSlashDayInNumber(flightDate);
        const multiCityFormFilterDate = await this.page.getMultiCityFormDate();
        return multiCityFormFilterDate.includes(flightFilterDate);
    }

    async clearFilter(): Promise<void> {
        const clearAllButton = element(by.css("[id$=-clearAll]"));
        await clearAllButton.click();
    }

    async searchFlightsWithoutFillingMCForm(): Promise<void> {
        const searchButton = element(by.css("[id$=-submit-multi]"));
        await searchButton.click();
    }

    async isErrorModalDisplayed(): Promise<boolean> {
        const errorModal = element(by.css(".Common-Errors-ErrorDialog-Dialog")).element(by.css("[id$=-dialog-content]"));
        return await errorModal.isDisplayed();
    }

    async getErrorMessages(messageNo: number): Promise<string> {
        const errorMessageTag = await this.getErrorModalErrorMessage(messageNo);
        return await errorMessageTag.getText();
    }

    async getErrorModalErrorMessage(messageNo: number): Promise<ElementFinder> {
        const errorMessages = element(by.css(".Common-Errors-ErrorDialog-Dialog")).all(by.css("[id$=-messages] li"));
        return await errorMessages.get(messageNo);
    }

    async closeErrorModal(): Promise<void> {
        const errorModal = element(by.css(".Common-Errors-ErrorDialog-Dialog")).all(by.css(".errorDialogCloseButton"));
        return await errorModal.click();
    }
}

export default FlightSearchResultPageObject;