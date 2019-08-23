import { browser, by, element, ElementArrayFinder } from "protractor";
import BasePageObject from "./basePageObject";

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
        return await browser.executeScript('return document.querySelector("[id$=-cabin-content] ul li").querySelector(".label").innerText');
    }

    async getCountOfDisplayedTakeOffSliders(): Promise<number> {
        const sliders = this.getTakeOffSliders();
        return this.getSliders(sliders);
    }

    getTakeOffSliders(): ElementArrayFinder {
        return element(by.css("[id$=-times-timesSection]")).all(by.css("[id$=-times-takeoff]")).first().all(by.css(".js-legSection.timesFilterSection"));
    }

    async getCountOfDisplayedLandingSliders(): Promise<number> {
        const landingSliderTab = element(by.css(".takeoffLandingTabs")).element(by.css("[id$=-times-Landing-label]"));
        await landingSliderTab.click();
        const sliders = this.getLandingSliders();
        return await this.getSliders(sliders);
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
}

export default FlightSearchResultPageObject;