import {browser, $, element, by, protractor, promise, ElementFinder, ElementArrayFinder, ProtractorExpectedConditions} from 'protractor';
import {CommonPage} from "./CommonPage";
import { kayakHelper } from './kayakHelper';

export class FlightResultsPage {

	kayakCommonPage: CommonPage = new CommonPage();
	helper: kayakHelper = new kayakHelper();
	expectedCondition: ProtractorExpectedConditions = protractor.ExpectedConditions;
	kayakUrl: string = "https://www.kayak.com/flights/NYC-LAX/2019-08-18/2019-08-25";	
	loadingClass: ElementFinder = element(by.css("div[class*=no-spin]"));
	flightPredictionGraph = element(by.css("div[class*='FlightQueryPricePrediction'] div[id$=advice]"));
	cheapestPriceTab: ElementFinder = element(by.css("a[id$='price_aTab']"));
	flightCount: ElementFinder = element(by.css("div[id$=resultsCount]"));
	flightCountLink: ElementFinder = element(by.css("div[id$=resultsCount] .showAll"));
	flightsTotalCount: ElementFinder = element(by.css("span[id$=counts-totalCount]"));
	stopsFilter: ElementArrayFinder = element.all(by.css("div[id$=stops-content] li"));
	airlinesFilter: ElementArrayFinder = element.all(by.css("div[id$=airlines-airlines-content] li"));
	bookingProvidersFilter: ElementArrayFinder = element.all(by.css("div[id$=providers-content] li"));
	cabinFilter: ElementArrayFinder = element.all(by.css("div[id$=cabin-content] li"));
	flightQualityFilter: ElementArrayFinder = element.all(by.css("div[id$=quality-section-content] li"));
	cabinTitle: ElementFinder = element(by.css("div[id$=cabin-title]"));
	flightQualityTitle: ElementFinder = element(by.css("div[id$=quality-section-title]"));
	bookingProvidersTitle: ElementFinder = element(by.css("div[id$=providers-title]"));
	stopsResetLink: ElementFinder = element(by.css("a[id$=stops-reset]"));
	cabinResetLink: ElementFinder = element(by.css("a[id$=cabin-reset]"));
	airlinesResetLink: ElementFinder = element(by.css("a[id$=airlines-reset]"));
	airportsResetLink: ElementFinder = element(by.css("a[id$=airports-section-reset]"));
	bookingProvidersResetLink: ElementFinder = element(by.css("a[id$=providers-reset]"));
	flightResults: ElementArrayFinder = element.all(by.css(".Flights-Results-FlightResultItem"));
	popupDialog: ElementFinder = element(by.css(".flightsDriveBy"));
	popupDialogCloseButton: ElementFinder = this.popupDialog.element(by.css(".Button-No-Standard-Style.close"));
	jetBlueAirlinePrice: ElementFinder = element(by.css["button[id$=B6-price]"]);
	jetBlueAirlineCheckBox: ElementFinder = element(by.css["input[id$=B6-check]"]);
	oneStopCheckIcon: ElementFinder = element(by.css("div[id$='-1-check-icon']"));
	oneStopCheckBox: ElementFinder = element(by.css("input[id$='1-check']"));
	departureAndReturnSameCheckIcon: ElementFinder = element(by.css("div[id$='sameair-check-icon']"));
	departureAndReturnSameCheckbox: ElementFinder = element(by.css("input[id$=sameair-check]"));
	ewrCheckIcon: ElementFinder = element(by.css("div[id$=EWR-check-icon]"));
	ewrCheckBox: ElementFinder = element(by.css("input[id$=sameair-check]"));
	economyCabinCheckIcon: ElementFinder = element(by.css("div[id$=e-check-icon]"));
	economoyCabinCheckBox: ElementFinder = element(by.css("input[id$=e-check]"));
	longFlightsCheckIcon: ElementFinder = element(by.css("div[id$='baditin-check-icon']"));
	longFlightCheckBox: ElementFinder = element(by.css("input[id$='baditin-check']"));
	nonStopFilter: ElementFinder = element(by.css("li[id$='-0']"));
	nonStopOnlyLink: ElementFinder = element(by.css("button[id$='0-only']"));
	nonStopCheckBox: ElementFinder = element(by.css("input[id$='0-check']"));	
	alaskaAirlineFilter: ElementFinder = element(by.css("li[id$='-0']"));
	alaskaAirlineOnlyLink: ElementFinder = element(by.css("button[id$='-AS-only']"));	
	alaskaAirlineCheckBox: ElementFinder = element(by.css("input[id$='AS-check']"));
	cheapoairBookingProviderPrice: ElementFinder = element(by.css("button[id$=-CHEAPOAIR-price]"));
	cheapoairBookingProviderCheckbox: ElementFinder = element(by.css("input[id$=CHEAPOAIR-check]"));

	async get(): Promise<void> {
		await browser.get(this.kayakUrl);
	}

	async nonAngularApplication(): Promise<void> {
		browser.ignoreSynchronization = await true;
	}

	async closePopupDialog(): Promise<void> {
		await this.kayakCommonPage.waitUntillElementAppears(this.popupDialog);
		await this.popupDialogCloseButton.click();
	}

	async getTotalFlights(): Promise<number> {
		let flightsTotalCount = await this.flightsTotalCount.getText();
		return Number(flightsTotalCount);
	}

	async getCheapestPrice(): Promise<number> {
		await this.kayakCommonPage.waitUntillElementAppears(this.cheapestPriceTab);
		return this.helper.getPrice(await this.cheapestPriceTab.getText());
	}

	async getFlightsCount(): Promise<string> {
		await this.kayakCommonPage.waitUntillElementAppears(this.flightCount);
		return this.flightCount.getText();
	}

	async oneStopChecked(): Promise<boolean> {
		return await this.oneStopCheckBox.getAttribute("aria-checked") === "true";
	}

	async clickOneStopCheckbox(): Promise<void> {
		let oneStopChecked = await this.oneStopChecked();
		if(!oneStopChecked) {
			this.oneStopCheckIcon.click();
		}
	}

	async sameDepartureAndReturnAirportChecked(): Promise<boolean> {
		return await this.departureAndReturnSameCheckbox.getAttribute("aria-checked") === "true";
	}

	async checkSameDepartureAndReturnAirport(): Promise<void> {
		let sameDepartureAndReturnChecked = await this.sameDepartureAndReturnAirportChecked();
		if(!sameDepartureAndReturnChecked) {
			await this.departureAndReturnSameCheckIcon.click();
		}
	}

	async uncheckSameDepartureAndReturnAirport(): Promise<void> {
		let sameDepartureAndReturnChecked = await this.sameDepartureAndReturnAirportChecked();
		if(sameDepartureAndReturnChecked) {
			await this.departureAndReturnSameCheckIcon.click();
		}
	}

	async ewrAirportChecked(): Promise<boolean> {
		return await this.ewrCheckBox.getAttribute("aria-checked") === "true";
	}

	async checkEwrAirport(): Promise<void> {
		let ewrAirportChecked = await this.ewrAirportChecked();
		if(!ewrAirportChecked) {
			await this.ewrCheckIcon.click();
		}
	}

	async clickBookingProviderResetLink(): Promise<void> {
		await this.bookingProvidersResetLink.click();
	}

	async bookingProviderResetLinkDisplayed(): Promise<void> {
		await this.bookingProvidersResetLink.isDisplayed();
	}

	async clickTopFlightsLink(): Promise<void> {
		await this.flightCountLink.click();
	}

	async clickResetCabinLink(): Promise<void> {
		await this.cabinResetLink.click();
	}

	async resetCabinLinkDisplayed(): Promise<void> {
		await this.cabinResetLink.isDisplayed();
	}

	async clickCabinTitle(): Promise<void> {
		let cabinExpand = await this.flightQualityTitle.getAttribute("aria-expanded");
		if(cabinExpand === "false") {
			await this.cabinTitle.click();
		}
	}

	async clickFlightQualityTitle(): Promise<void> {
		let flightQualityExpand = await this.flightQualityTitle.getAttribute("aria-expanded");
		if(flightQualityExpand === "false") {
			await this.flightQualityTitle.click();
		}
	}

	async clickBookingSitesTitle(): Promise<void> {
		let bookingExpand = await this.bookingProvidersTitle.getAttribute("aria-expanded");
		if(bookingExpand === "false") {
			await this.bookingProvidersTitle.click();
		}
	}

	async clickJetBluePrice(): Promise<void> {
		await this.jetBlueAirlinePrice.click();
	}

	async jetBlueAirlineChecked(): Promise<boolean> {
		return await this.jetBlueAirlineCheckBox.getAttribute("aria-checked") === "true";
	}

	async longFlightsFilterChecked(): Promise<boolean> {
		return await this.longFlightCheckBox.getAttribute("aria-checked") === "true";
	}

	async checkLongFlightsFilter(): Promise<void> {
		await this.clickFlightQualityTitle();
		let longFlightsFilterChecked = await this.longFlightsFilterChecked();
		if(!longFlightsFilterChecked) {
			this.longFlightCheckBox.click();
		}
	}

	async stopResetLinkDisplayed(): Promise<boolean> {
		await this.kayakCommonPage.waitUntillElementAppears(this.stopsResetLink);
		return this.stopsResetLink.isDisplayed();
	}

	async hoverAndClickNonStopOnlyLink(): Promise<void> {
		await browser.actions().mouseMove(this.nonStopFilter).perform();
		await this.kayakCommonPage.waitUntillElementAppears(this.nonStopOnlyLink);
		await this.nonStopOnlyLink.click();
	}

	async nonStopChecked(): Promise<boolean> {
		return await this.nonStopCheckBox.getAttribute("aria-checked") === "true";
	}

	async economyCabinChecked(): Promise<boolean> {
		return await this.economoyCabinCheckBox.getAttribute("aria-checked") === "true";
	}

	async uncheckEconomyCabin(): Promise<void> {
		await this.clickCabinTitle();
		let economyCabinChecked = await this.economyCabinChecked();
		if(economyCabinChecked) {
			this.economoyCabinCheckBox.click();
		}
	}

	async selectAlaskaAirlines(): Promise<void> {
		await browser.actions().mouseMove(this.alaskaAirlineFilter).perform();
		await this.kayakCommonPage.waitUntillElementAppears(this.alaskaAirlineOnlyLink);
		await this.alaskaAirlineOnlyLink.click();
	}

	async alaskaAirlinesFilterChecked(): Promise<boolean> {
		return await this.alaskaAirlineCheckBox.getAttribute("aria-checked") === "true";
	}
	async farePredictionPriceDisplayed(): Promise<boolean> {
		await browser.wait(this.kayakCommonPage.patternToBePresentInElement(this.flightPredictionGraph, /\w\w+/i));
		return this.flightPredictionGraph.isDisplayed();
	}

	async getTargetedArrayFromResults(selector: string) {
		await browser.wait(this.expectedCondition.invisibilityOf(this.loadingClass), 30000);
		return this.flightResults.then(async function(results) {
			let elementTextContents: string[] = await [];
			for(let result of results) {
				let elementTextContent: string = await result.element(by.css(selector)).getText();
				elementTextContents.push(elementTextContent.trim());
			}
			return elementTextContents;
		});
	}

	async resultsContainNonStopOnly(): Promise<boolean> {
		let stops: string[] = await this.getTargetedArrayFromResults(".section.stops");
		return (stops.indexOf("nonstop") === -1) ? false : true;
				
	}

	async resultsContainNonStopAndOneStopOnly(): Promise<boolean> {
		let stops: string[] = await this.getTargetedArrayFromResults(".section.stops");
		return ((stops.indexOf("nonstop") === -1) && (stops.indexOf("1 stop") === -1)) ? false : true;
	}

	async resultsContainJetBlueAirwaysOnly(): Promise<boolean> {
		let airlines: string[] = await this.getTargetedArrayFromResults(".section.times .bottom");
		return airlines.indexOf("JetBlue") ? false : true;
	}

	async resultsNotContainEWRAirport(): Promise<boolean> {
		let departureAiports: string[] = await this.getTargetedArrayFromResults("div[id$=leg-0] .section.duration .bottom span");
		return departureAiports.indexOf("EWR") !== -1 ? false : true;
				
	}

	async resultsContainDepartureAndReturnSame(): Promise<boolean> {
		let departures: string[] = await this.getTargetedArrayFromResults("div[id$=leg-0] .section.duration .bottom span:nth-child(3)");
		let returns: string[] = await this.getTargetedArrayFromResults("div[id$=leg-1] .section.duration .bottom span:nth-child(1)");
		for (let departure in departures) {
			if(returns.indexOf(departure) === -1) {
				return false;
			}	
		}
		return true;
	}

	async resultsContainDepartureAndReturnSameAndDifferent(): Promise<boolean> {
		let departures: string[] = await this.getTargetedArrayFromResults("div[id$=leg-0] .section.duration .bottom span:nth-child(3)");
		let returns: string[] = await this.getTargetedArrayFromResults("div[id$=leg-1] .section.duration .bottom span:nth-child(1)");
		for (let departure in departures) {
			if(returns.indexOf(departure) === -1) {
				return true;
			}	
		}
		return false;
	}

	async resultsContainsAlaskaAirlinesOnly(): Promise<boolean> {
		let airlines: string[] = await this.getTargetedArrayFromResults(".providerName");
		return airlines.indexOf("Alaska Airlines") === -1 ? false : true;
	}

	async resultsContainsAllProviders(): Promise<boolean> {
		let airlines: string[] = await this.getTargetedArrayFromResults(".providerName");
		return (airlines.indexOf("American Airlines") === -1) ? false : true;
	}

	async resultsNotContainEconomyCabins(): Promise<boolean> {
		let cabins: string[] = await this.getTargetedArrayFromResults("span[id$=toolTipTarget]");
		return (cabins.indexOf("Economy") !== -1) ? false : true;
	}

	async resultsContainAllCabins(): Promise<boolean> {
		let cabins: string[] = await this.getTargetedArrayFromResults("span[id$=toolTipTarget]");
		return (cabins.indexOf("Economy") === -1 && cabins.indexOf("Saver") === -1 && cabins.indexOf("Main") === -1) 
		? false : true;	
	}

	async resetAllFilters(): Promise<boolean> {
		let stopsResetLinkDisplayed = await this.stopsResetLink.isDisplayed();
		let cabinResetLinkDisplayed = await this.cabinResetLink.isDisplayed();
		let airlinesResetLinkDisplayed = await this.airlinesResetLink.isDisplayed();
		let airportsResetLinkDisplayed = await this.airportsResetLink.isDisplayed();
		let bookingProvidersResetLinkDisplayed = await this.bookingProvidersResetLink.isDisplayed();
		if(!stopsResetLinkDisplayed && !cabinResetLinkDisplayed && !airlinesResetLinkDisplayed && !airportsResetLinkDisplayed && !bookingProvidersResetLinkDisplayed) {
			return true;
		}
		else {
			return false;
		}
	}

	async getCheapoAirBookingProviderPrice(): Promise<number> {
		let price = await this.cheapoairBookingProviderPrice.getText();
		return Number(price.split("$")[1]);
	}

	async cheapoAirBookingProviderChecked(): Promise<boolean> {
		return await this.cheapoairBookingProviderCheckbox.getAttribute("aria-checked" ) === "true";
	}

	async clickCheapoAirBookingProviderPrice(): Promise<void> {
		await this.cheapoairBookingProviderPrice.click();
	}

	async airportStopsCheck(selector: string, attribute: string = null) {
		return this.stopsFilter.then(async function(stops) {
			for (let stop of stops) {
				await browser.actions().mouseMove(stop).mouseMove(stop).perform();
				let stopChecked: string = await (attribute) ? stop.element(by.css(selector)).getAttribute(attribute) : stop.element(by.css(selector)).getText();
				if(!stopChecked || stopChecked === "false") {
					return false;
				}
			}
			return true;
		});
	}

	async airportStopFiltersChecked(): Promise<boolean> {
		return this.airportStopsCheck("input", "aria-checked");
	}

	async airportStopFiltersContainPrices(): Promise<boolean> {
		return this.airportStopsCheck(".price");
	}
	
	async airportStopFiltersHighlightedAndAppearOnlyOnHover(): Promise<boolean> {
		let that = await this;
		return this.stopsFilter.then(async function(stops) {
			for (let stop of stops) {
				await browser.actions().mouseMove(stop).mouseMove(stop).perform();
				await browser.wait(that.expectedCondition.visibilityOf(stop.element(by.css("button[id$='-only']"))), 30000);
				let onlyLink: boolean = await stop.element(by.css("button[id$='-only']")).isPresent();
				let highlightedColor: string = await stop.getCssValue("background-color");
				if(!onlyLink && highlightedColor !== "rgba(219, 238, 255, 1)") {
					return false;
				}
			}
			return true;
		});
	}
}