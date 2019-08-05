import {browser, $, element, by, protractor, promise, ElementFinder, ElementArrayFinder, ProtractorExpectedConditions, ExpectedConditions, Key} from 'protractor';
import { Helper } from './Helper';
var dragAndDrop = require('html-dnd').code;

export class BookingProviderPage {
    originAirport = element(by.css("input[id$=FlightOrigin]"));
    destinationAirport = element(by.css("input[id$=FlightDestination]"));
    departureDate = element(by.css("input[class*=js-date_input]"));


    async switchTab(): Promise<void> {
		browser.getAllWindowHandles().then((handles) => {
			if(handles.length > 1) {
				browser.driver.switchTo().window(handles[1]);
			}
		});
    }
    
    async originAirportDisplayed(): Promise<boolean> {
        await browser.wait(ExpectedConditions.visibilityOf(this.originAirport), 20000);
        return await this.originAirport.isDisplayed();
    }

    async getoriginAirport(): Promise<string> {
        return await this.originAirport.getText();
    }

    async getDestinationAirport(): Promise<string> {
        return await this.destinationAirport.getText();
    }

    async getDepartureDate(): Promise<string> {
        let departureDate = await this.departureDate.getAttribute("value");
        return await departureDate.split(" ")[0];
    }
}