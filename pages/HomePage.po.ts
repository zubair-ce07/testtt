import {browser, element, by, ElementFinder, ExpectedConditions} from 'protractor';
import HomePageElements from "../pageElements/HomePageElements";
import moment from 'moment';
export default class HomePage {
    homePageElementsObj = new HomePageElements();
    private EC: any = ExpectedConditions;
    async loadHomePage (): Promise<void> {
        await browser.get('https://global.momondo.com/flight-search/LON-NYC/2019-08-24/2019-09-22?sort=price_a');
    };
    async getOrigin (): Promise<string> {
        return await this.homePageElementsObj.getFlightOrigin();
    };
    async getDestination (): Promise<string> {
        return await this.homePageElementsObj.getFlightDestination();
    };
    async getDepartureDate (): Promise<string> {
        return await this.homePageElementsObj.getFlightDepartureDate();
    };
    async getReturnDate (): Promise<string> {
        return await this.homePageElementsObj.getFlightReturnDate();
    };
    async getTravelers (): Promise<string> {
        return await this.homePageElementsObj.getFlightTravelers();
    };
    async isGraphVisible (): Promise<boolean> {
        const graphElement = await this.homePageElementsObj.getGraph();
        this.waitForElementToBeVisible(graphElement);
        return graphElement.isDisplayed();
    };
    selectTripType (tripType: string):void {
        element(by.css("label[title='"+tripType+"']")).click();
    };
    async getMainVisibleGraphCount (operationType: string): Promise<number> {
        await this.homePageElementsObj.clickSearchBtn();
        let allVisibleGraphs = await this.homePageElementsObj.getAllVisibleGraphs();
        if(operationType === 'first_half') {
            this.waitForElementToBeInvisible(allVisibleGraphs.get(1));
        } else {
            this.waitForElementToBeVisible(allVisibleGraphs.get(1));
        }
        return allVisibleGraphs.count();
    };
    async selectDateFromCalendar (): Promise<void> {
        await this.homePageElementsObj.clickFlightReturnDate();
        const newCalendarDateElement = this.homePageElementsObj.getNewCalendarDate();
        this.waitForElementToBeClickable(newCalendarDateElement);
        await this.homePageElementsObj.clickNewCalendarDate();
        this.waitForElementToBeInvisible(newCalendarDateElement);
    };
    async getGraphBarTooltipText (): Promise<string> {
        await this.homePageElementsObj.hoverOverGraphBar();
        const tooltip = await this.homePageElementsObj.getGraphBarTooltip();
        await this.waitForElementToBeVisible(tooltip);
        return tooltip.getText();
    };
    async getNewDate (): Promise<string> {
        const selectedBar = await this.homePageElementsObj.getSelectedGraphBar();
        await this.waitForElementToBeClickable(selectedBar);
        const pre_selectedDate = await this.homePageElementsObj.getSelectedGraphBarDate();
        return moment(pre_selectedDate).add(2, 'days').format('YYYY-MM-DD');
    };
    async getNewSelectedGraphBar (barDate: string): Promise<any> {
        const newGraphBar = await this.homePageElementsObj.getNewGraphBar(barDate);
        await this.waitForElementToBeClickable(newGraphBar);
        await newGraphBar.click();
        return await newGraphBar;
    };
    // @ts-ignore
    async getSelectedBarStatus (newSelectGraphBar): Promise<string> {
        this.waitForElementToBeVisible(newSelectGraphBar);
        browser.wait(async () => {
            const SelectedGraphBarAttributes = await newSelectGraphBar.getAttribute('class');
                if(SelectedGraphBarAttributes.includes('selected')){
                    return true
                }
        },5000);
        return newSelectGraphBar.getAttribute('class');
    };
    async isSelectedBarPriceVisible (): Promise<boolean> {
        const selectedBarPrice = await this.homePageElementsObj.getSelectedBarPrice();
        await this.waitForElementToBeVisible(selectedBarPrice);
        return selectedBarPrice.isDisplayed();
    };
    async isSelectedPriceLabelVisible(): Promise<boolean> {
        const selectedPricelabel = await this.homePageElementsObj.getSelectedPriceLabel();
        await this.waitForElementToBeVisible(selectedPricelabel);
        return selectedPricelabel.isDisplayed();
    };
    async isSearchBtnVisible (): Promise<boolean> {
        const searchBtn = await this.homePageElementsObj.getSearchTheseDaysBtn();
        await this.waitForElementToBeVisible(searchBtn);
        return searchBtn.isDisplayed();
    };
    async searchTheseDays(): Promise<void> {
        const searchTheseDaysButton = await this.homePageElementsObj.getSearchTheseDaysBtn();
        await this.homePageElementsObj.clickSearchTheseDaysBtn();
        await this.waitForElementToBeInvisible(searchTheseDaysButton);
    };
    async showDetails(): Promise<void> {
        const allVisibleGraphs = await this.homePageElementsObj.getAllVisibleGraphs();
        await this.waitForElementToBeVisible(allVisibleGraphs.get(1));
        const showDetailsBtn = await this.homePageElementsObj.getShowDetailsBtn();
        await this.waitForElementToBeClickable(showDetailsBtn);
        await this.homePageElementsObj.clickShowDetailsBtn();
    };
    async getDepartureDateFromDetailsPanel (): Promise<string> {
        let detailsPanel = await this.homePageElementsObj.getDetailsPanel();
        detailsPanel = detailsPanel.first();
        await this.waitForElementToBeVisible(detailsPanel);
        const detailsPanelDepartureDate = await this.homePageElementsObj.getDetailsPanelDepartureDate();
        await this.waitForElementToBeVisible(detailsPanelDepartureDate);
        await this.waitForElementToBeVisible(detailsPanelDepartureDate.element(by.css('div')));
        return await detailsPanelDepartureDate.element(by.css('div')).getText();
    };
    isPricesShownLabelVisible (): ElementFinder {
        return this.homePageElementsObj.getSelectedPriceLabel();
    };
    isSearchTheseDaysBtnVisible (): ElementFinder {
        return this.homePageElementsObj.getSearchTheseDaysBtn();
    };

    // Common Functions
    waitForElementToBeVisible(element: any): any {
        browser.wait(this.EC.visibilityOf(element),5000);
    }
    waitForElementToBeInvisible(element: any): any {
        browser.wait(this.EC.invisibilityOf(element),5000);
    }
    waitForElementToBeClickable(element: any): any {
        browser.wait(this.EC.elementToBeClickable(element),5000);
    }
}