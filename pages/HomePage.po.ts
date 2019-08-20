import {browser, element, by, ElementFinder, ExpectedConditions} from 'protractor';
import HomePageElements from "../pageElements/HomePageElements";
import moment from 'moment';
export default class HomePage {
    homePageElementsObj = new HomePageElements();
    private EC: any = ExpectedConditions;
    async loadHomePage (): Promise<void> {
        await browser.get('https://global.momondo.com/flight-search/LON-NYC/2019-08-24/2019-09-22?sort=price_a');
    };
    getOrigin (): Promise<string> {
        return this.homePageElementsObj.getFlightOrigin();
    };
    getDestination (): Promise<string> {
        return this.homePageElementsObj.getFlightDestination();
    };
    getDepartureDate (): Promise<string> {
        return this.homePageElementsObj.getFlightDepartureDate();
    };
    getReturnDate (): Promise<string> {
        return this.homePageElementsObj.getFlightReturnDate();
    };
    getTravelers (): Promise<string> {
        return this.homePageElementsObj.getFlightTravelers();
    };
    isGraphVisible (): Promise<boolean> {
        const graphElement = this.homePageElementsObj.getGraph();
        this.waitForElementToBeVisible(graphElement);
        return graphElement.isDisplayed();
    };
    selectTripType (tripType: string):void {
        element(by.css("label[title='"+tripType+"']")).click();
    };
    getMainVisibleGraphCount (operationType: string): Promise<number> {
        this.homePageElementsObj.clickSearchBtn();
        let allVisibleGraphs = this.homePageElementsObj.getAllVisibleGraphs();
        if(operationType === 'first_half') {
            this.waitForElementToBeInvisible(allVisibleGraphs.get(1));
        } else {
            this.waitForElementToBeVisible(allVisibleGraphs.get(1));
        }
        return allVisibleGraphs.count();
    };
    selectDateFromCalendar (): void {
        this.homePageElementsObj.clickFlightReturnDate();
        const newCalendarDateElement = this.homePageElementsObj.getNewCalendarDate();
        this.waitForElementToBeClickable(newCalendarDateElement);
        this.homePageElementsObj.clickNewCalendarDate();
        this.waitForElementToBeInvisible(newCalendarDateElement);
    };
    getGraphBarTooltipText (): Promise<string> {
        this.homePageElementsObj.hoverOverGraphBar();
        const tooltip = this.homePageElementsObj.getGraphBarTooltip();
        this.waitForElementToBeVisible(tooltip);
        return tooltip.getText();
    };
    async getNewDate (): Promise<string> {
        const selectedBar = this.homePageElementsObj.getSelectedGraphBar();
        this.waitForElementToBeClickable(selectedBar);
        const pre_selectedDate = this.homePageElementsObj.getSelectedGraphBarDate();
        return moment(pre_selectedDate).add(2, 'days').format('YYYY-MM-DD');
    };
    async getNewSelectedGraphBar (barDate: string): Promise<any> {
        const newGraphBar = this.homePageElementsObj.getNewGraphBar(barDate);
        this.waitForElementToBeClickable(newGraphBar);
        await newGraphBar.click();
        return newGraphBar;
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
        return newSelectGraphBar.getAttribute('class')
    };
    async isSelectedBarPriceVisible (): Promise<boolean> {
        const selectedBarPrice = this.homePageElementsObj.getSelectedBarPrice();
        this.waitForElementToBeVisible(selectedBarPrice);
        return await selectedBarPrice.isDisplayed();
    };
    async isSelectedPriceLabelVisible(): Promise<boolean> {
        const selectedPricelabel = this.homePageElementsObj.getSelectedPriceLabel();
        this.waitForElementToBeVisible(selectedPricelabel);
        return await selectedPricelabel.isDisplayed();
    };
    async isSearchBtnVisible (): Promise<boolean> {
        const searchBtn = this.homePageElementsObj.getSearchTheseDaysBtn();
        this.waitForElementToBeVisible(searchBtn);
        return await searchBtn.isDisplayed();
    };
    async searchTheseDays(): Promise<void> {
        const searchTheseDaysButton = this.homePageElementsObj.getSearchTheseDaysBtn();
        this.homePageElementsObj.clickSearchTheseDaysBtn();
        this.waitForElementToBeInvisible(searchTheseDaysButton);
    };
    async showDetails(): Promise<void> {
        const allVisibleGraphs = this.homePageElementsObj.getAllVisibleGraphs();
        this.waitForElementToBeVisible(allVisibleGraphs.get(1));
        const showDetailsBtn = this.homePageElementsObj.getShowDetailsBtn();
        this.waitForElementToBeClickable(showDetailsBtn);
        this.homePageElementsObj.clickShowDetailsBtn();
    };
    async getDepartureDateFromDetailsPanel (): Promise<string> {
        let detailsPanel = this.homePageElementsObj.getDetailsPanel();
        detailsPanel = detailsPanel.first();
        this.waitForElementToBeVisible(detailsPanel);
        const detailsPanelDepartureDate = this.homePageElementsObj.getDetailsPanelDepartureDate();
        this.waitForElementToBeVisible(detailsPanelDepartureDate);
        this.waitForElementToBeVisible(detailsPanelDepartureDate.element(by.css('div')));
        return detailsPanelDepartureDate.element(by.css('div')).getText();
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