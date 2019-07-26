import {browser, $, element, by, protractor, promise, ElementFinder, ElementArrayFinder, ProtractorExpectedConditions} from 'protractor';
import {CommonPage} from "./CommonPage"
import { kayakHelper } from './kayakHelper';

export class FlightResultsPage {

	kayakCommonPage: CommonPage = new CommonPage();
	helper: kayakHelper = new kayakHelper();
	expectedCondition: ProtractorExpectedConditions = protractor.ExpectedConditions;
	kayakUrl: string = "https://www.kayak.com/flights/NYC-LAX/2019-08-18/2019-08-25";	
	loadingClass: ElementFinder = element(by.css("div[class*=no-spin]"));
	flightPredictionGraph = element(by.css("div[class*='FlightQueryPricePrediction'] div[id$=advice]"));
	cheapestPrice: ElementFinder = element(by.css("a[id$='price_aTab']"));
	flightCount: ElementFinder = element(by.css("div[id$=resultsCount]"));
	flightCountLink: ElementFinder = element(by.css("div[id$=resultsCount] .showAll"));
	flightsTotalCount: ElementFinder = element(by.css("span[id$=counts-totalCount]"));
	stopsFilter: ElementArrayFinder = element.all(by.css("div[id$=stops-content] li"));
	airlinesFilter: ElementArrayFinder = element.all(by.css("div[id$=airlines-airlines-content] li"));
	bookingProvidersFilter: ElementArrayFinder = element.all(by.css("div[id$=providers-content] li"));
	cabinFilter: ElementArrayFinder = element.all(by.css("div[id$=cabin-content] li"));
	qualityFilter: ElementArrayFinder = element.all(by.css("div[id$=quality-section-content] li"));
	stopsInResults: ElementArrayFinder = element.all(by.css(".section.stops"));
	sameDepartAndReturnCheckbox: ElementFinder = element(by.css("div[id$=sameair-check-icon]"));
	ewrCheckbox: ElementFinder = element(by.css("div[id$=EWR-check-icon]"));
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

	async get(): Promise<void> {
		await browser.get(this.kayakUrl);
	}

	async isNonAngularApplication(): Promise<void> {
		browser.ignoreSynchronization = await true;
	}

	async maximizeBrowser(): Promise<void> {
		await browser.manage().window().setSize(1600, 1000);
	}

	async closePopupDialog(): Promise<void> {
		await this.kayakCommonPage.waitUntillElementAppears(this.popupDialog)
		await this.popupDialogCloseButton.click();
	}

	async getTotalFlights(): Promise<number> {
		return this.flightsTotalCount.getText().then(function(totalFlights) {
			return Number(totalFlights);
		});
	}

	async getCheapestPrice(): Promise<number> {
		await this.kayakCommonPage.waitUntillElementAppears(this.cheapestPrice);
		return this.helper.getPrice(await this.cheapestPrice.getText());
	}

	async getFlightsCount(): Promise<string> {
		await this.kayakCommonPage.waitUntillElementAppears(this.flightCount);
		return this.flightCount.getText();
	}

	async getBookingProviderFilterPrice(): Promise<number> {
		let that = await this;
		return this.bookingProvidersFilter.then(async function(providers) {
			for(let provider of providers) {
				await browser.actions().mouseMove(provider).perform();
				let PriceText: string = await provider.element(by.css("button[id$=-price]")).getText();
				if(PriceText.trim()) {
					return await that.helper.getPrice(PriceText);
				}
			}
		});
	}

	async clickOneStopCheckbox(): Promise<void> {
		await this.stopsFilter.then(function(stops) {
			stops[1].element(by.css("div[id$=check-icon]")).click();
		});
	}

	async checkSameDepartAndReturn(): Promise<void> {
		let isSameDepartAndReturnChecked = await this.sameDepartAndReturnCheckbox.getAttribute("aria-checked");
		if(isSameDepartAndReturnChecked === "false") {
			await this.sameDepartAndReturnCheckbox.click();
		}
	}

	async unCheckSameDepartAndReturn(): Promise<void> {
		let isSameDepartAndReturnChecked = await this.sameDepartAndReturnCheckbox.getAttribute("aria-checked");
		if(isSameDepartAndReturnChecked === "true") {
			await this.sameDepartAndReturnCheckbox.click();
		}
	}

	async clickEWRCheckbox(): Promise<void> {
		await this.ewrCheckbox.click();
	}

	async clickBookingProviderResetLink(): Promise<void> {
		await this.bookingProvidersResetLink.click();
	}

	async clickTopFlightsLink(): Promise<void> {
		await this.flightCountLink.click();
	}

	async clickResetCabinLink(): Promise<void> {
		await this.cabinResetLink.click();
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
		return this.airlinesFilter.then(async function(airlines) {
			for(let airline of airlines) {
				let airlineText: string = await airline.element(by.css("label[id$=check-label]")).getText();
				airlineText = airlineText.trim();
				if(airlineText.indexOf("JetBlue") !== -1) {
					await airline.element(by.css("button[id$=-price")).click();
				}
			}
		});
	}

	async clickLongFlightsFilter(): Promise<void> {
		return this.qualityFilter.then(async function(flights) {
			for(let flight of flights) {
				let flightText: string = await flight.element(by.css("label[id$=check-label]")).getText();
				flightText = flightText.trim();
				if(flightText.indexOf("longer flights") !== -1) {
					await flight.element(by.css("div[id$=check-icon]")).click();
				}
			}
		});
	}

	async isStopFiltersChecked(): Promise<boolean> {
		return this.stopsFilter.then(async function(stops) {
			for (let stop of stops) {
				const stopChecked: string = await stop.element(by.tagName("input")).getAttribute("aria-checked");
				if(stopChecked === "false") {
					return false;
				}
			}
			return true;
		});
	}

	async isStopFiltersContainPrices(): Promise<boolean> {
		return this.stopsFilter.then(async function(stops) {
			for(let stop of stops) {
				const price: string = await stop.element(by.className("price")).getText();
				if(!price.match(/\$((?:\d|\,)*\.?\d+)/g)) {
					return false;
				}
			}
			return true;
		});
	}
	
	async isStopFiltersHighlightedAndShowOnlyOnHover(): Promise<boolean> {
		let that = await this;
		return this.stopsFilter.then(async function(stops) {
			for (let stop of stops) {
				await browser.actions().mouseMove(stop).mouseMove(stop).perform();
				await browser.wait(that.expectedCondition.visibilityOf(stop.element(by.css("button[id$='-only']"))), 30000);
				const onlyLink: boolean = await stop.element(by.css("button[id$='-only']")).isPresent();
				if(!onlyLink) {
					return false
				}
			}
			return true;
		});
	}

	async isResetLinkAppeared(): Promise<boolean> {
		await this.kayakCommonPage.waitUntillElementAppears(this.stopsResetLink);
		return this.stopsResetLink.isDisplayed();
	}

	async hoverAndClickNonStopOnlyLink(): Promise<void> {
		let that = await this;
		await this.stopsFilter.then(async function(stops) {
			for (let stop of stops) {
				await browser.actions().mouseMove(stop).perform();
				let stopText = await stop.element(by.css("label[id$=check-label]")).getText();
				if(stopText.trim() === "Nonstop") {
					await browser.wait(that.expectedCondition.visibilityOf(stop.element(by.css("button[id$='-only']"))), 30000);
					await stop.element(by.css("button[id$='-only']")).click();
					return;
				}
			}
		});
	}

	async uncheckEconomyFilter(): Promise<void> {
		return this.cabinFilter.then(async function(cabins) {
			for(let cabin of cabins) {
				let cabinText: string = await cabin.element(by.css("label[id$=check-label]")).getText();
				if(cabinText.trim().indexOf("Economy") !== -1) {
					await cabin.element(by.css("div[id$=check-icon]")).click();
				}
			}
		});
	}

	async selectAlaskaAirlines(): Promise<void> {
		let that = await this;
		return this.bookingProvidersFilter.then(async function(providers) {
			for(let provider of providers) {
				await browser.actions().mouseMove(provider).perform();
				let providerText: string = await provider.element(by.css("label[id$=check-label]")).getText();
				if(providerText.trim().indexOf("Alaska Airlines") !== -1) {
					await browser.wait(that.expectedCondition.visibilityOf(provider.element(by.css("button[id$='-only']"))), 30000);
					await provider.element(by.css("button[id$=-only")).click();
					return;
				}
			}
		});
	}

	async isPredictionPriceDisplayed(): Promise<boolean> {
		browser.wait(this.kayakCommonPage.patternToBePresentInElement(this.flightPredictionGraph, /buy now/i));
		if(this.flightPredictionGraph.isDisplayed()) {
			return true;
		}
	}

	async isResultsContainNonStopOnly(): Promise<boolean> {
		await browser.wait(this.expectedCondition.invisibilityOf(this.loadingClass), 10000);
		return await this.stopsInResults.then(async function(stops) {
			for(let stop of stops) {
				let stopText: string = await stop.getText();
				if(stopText.indexOf("nonstop") === -1) {
					return false;
				}
			}
			return true;
		});
	}

	async isResultsContainNonStopAndOneStopOnly(): Promise<boolean> {
		await browser.wait(this.expectedCondition.invisibilityOf(this.loadingClass), 10000);
		return this.stopsInResults.then(async function(results) {
			for(let result of results) {
				let stopText: string = await result.getText();
				if((stopText.trim().indexOf("nonstop") === -1) && (stopText.indexOf("1 stop") === -1)) {
					return false;
				}
			}
			return true;
		});
	}

	async isResultsContainJetBlueAirwaysOnly(): Promise<boolean> {
		await browser.wait(this.expectedCondition.invisibilityOf(this.loadingClass), 10000);
		return this.flightResults.then(async function(results) {
			for(let result of results) {
				let airline: string = await result.element(by.css(".section.times .bottom")).getText();
				if(airline.trim().indexOf("JetBlue") === -1) {
					console.log(airline);
					return false;
				}
			}
			return true;
		});
	}

	async isResultsNotContainEWRAirport(): Promise<boolean> {
		await browser.wait(this.expectedCondition.invisibilityOf(this.loadingClass), 10000);
		return this.flightResults.then(async function(results) {
			for(let result of results) {
				let departed: string = await result.element(by.css("div[id$=leg-0")).element(by.css(".section.duration .bottom")).getText();
				departed = departed.split("‐")[0].trim()
				if(departed.indexOf("EWR") !== -1) {
					return false;
				}
			}
			return true;
		});
	}

	async isResultsContainDepartAndReturnSame(): Promise<boolean> {
		await browser.wait(this.expectedCondition.invisibilityOf(this.loadingClass), 10000);
		return this.flightResults.then(async function(results) {
			for(let result of results) {
				let departed: string = await result.element(by.css("div[id$=leg-0")).element(by.css(".section.duration .bottom")).getText();
				let returned: string = await result.element(by.css("div[id$=leg-1")).element(by.css(".section.duration .bottom")).getText();
				departed = await departed.split("‐")[1].trim();
				returned = await returned.split("‐")[0].trim();
				if(returned.indexOf(departed) === -1) {
					return false;
				}	
			}
			return true;
		});
	}

	async isResultsContainDepartAndReturnSameAndDifferent(): Promise<boolean> {
		await browser.wait(this.expectedCondition.invisibilityOf(this.loadingClass), 10000);
		return this.flightResults.then(async function(results) {
			for(let result of results) {
				let departed: string = await result.element(by.css("div[id$=leg-0")).element(by.css(".section.duration .bottom")).getText();
				let returned: string = await result.element(by.css("div[id$=leg-1")).element(by.css(".section.duration .bottom")).getText();
				departed = await departed.split("‐")[1].trim();
				returned = await returned.split("‐")[0].trim();
				if(returned.indexOf(departed) === -1) {
					return true;
				}	
			}
			return false;
		});
	}

	async isResultsContainsAlaskaAirlinesOnly(): Promise<boolean> {
		await browser.wait(this.expectedCondition.invisibilityOf(this.loadingClass), 10000);
		return this.flightResults.then(async function(results) {
			for(let result of results) {
				let airline: string = await result.element(by.css(".providerName")).getText();
				airline = await airline.trim();
				if(airline.indexOf("Alaska Airlines") === -1) {
					return false;
				}
			}
			return true;
		});
	}

	async getAllProvidersNames(): Promise<string[]> {
		return this.bookingProvidersFilter.then(async function(providers) {
			let providerNames: string[] = [];
			for(let provider of providers) {
				let providerText: string = await provider.element(by.css("label[id$=-check-label]")).getText();
				await providerNames.push(providerText);
			}
			return providerNames;
		});
	}

	async isResultsContainsAllProviders(): Promise<boolean> {
		await browser.wait(this.expectedCondition.invisibilityOf(this.loadingClass), 10000);
		let providerNames: string[] = await this.getAllProvidersNames();
		return this.flightResults.then(async function(results) {
			for(let result of results) {
				let airline: string = await result.element(by.css(".providerName")).getText();
				airline = await airline.trim();
				if(providerNames.indexOf(airline) === -1) {
					return false;
				}
			}
			return true;
		});
	}

	async isResultsNotContainEconomyCabins(): Promise<boolean> {
		await browser.wait(this.expectedCondition.invisibilityOf(this.loadingClass), 10000);
		return this.flightResults.then(async function(results) {
			for(let result of results) {
				let cabinExists: boolean =  await result.element(by.css("span[id$=toolTipTarget]")).isPresent()
				if(cabinExists) {
					let cabin: string = await result.element(by.css("span[id$=toolTipTarget]")).getText();
					if(cabin.trim().indexOf("Economy") !== -1) {
						return false;
					}
				}
			}
			return true;
		});
	}

	async isResultsContainAllCabins(): Promise<boolean> {
		await browser.wait(this.expectedCondition.invisibilityOf(this.loadingClass), 10000);
		return this.flightResults.then(async function(results) {
			for(let result of results) {
				let cabinExists: boolean =  await result.element(by.css("span[id$=toolTipTarget]")).isPresent()
				if(cabinExists) {
					let cabin: string = await result.element(by.css("span[id$=toolTipTarget]")).getText();
					if(cabin.trim().indexOf("Economy") === -1 && cabin.trim().indexOf("Saver") === -1 && cabin.trim().indexOf("Main") === -1) {
						return false;
					}
				}
			}
			return true;
		});
	}

	async isAllFiltersReset(): Promise<boolean> {
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
}