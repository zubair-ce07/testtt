import {browser, ElementFinder, ExpectedConditions, ProtractorExpectedConditions} from "protractor";

export default class CommonHelper {
    EC: ProtractorExpectedConditions = ExpectedConditions;
    email: string = 'junaid.nazir@arbisoft.com';
    password: string = 'Oplay1840';
    tripDestination: string = 'Boston';
    tripName: string = 'Super trip to Boston';
    tripDestinationEdit: string = 'Paris';
    tripNameEdit: string = 'Birthday in Paris';
    async waitForElementToBeVisible(element: ElementFinder): Promise<any> {
        await browser.wait(this.EC.visibilityOf(element), 5000)
    }
    async waitForElementToBeInvisible(element: ElementFinder): Promise<any> {
        await browser.wait(this.EC.invisibilityOf(element), 5000)
    }
    async waitForElementToBeClickable(element: ElementFinder): Promise<any> {
        await browser.wait(this.EC.elementToBeClickable(element), 5000)
    }
}