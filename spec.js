"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const HomePage_po_1 = __importDefault(require("./pages/HomePage.po"));
const protractor_1 = require("protractor");
const moment_1 = __importDefault(require("moment"));
describe('Protractor Demo App', () => {
    protractor_1.browser.ignoreSynchronization = true;
    let SELECTED_DATE = '';
    let homePageObj = new HomePage_po_1.default();
    homePageObj.loadHomePage();
    it('Should display ‘London (LON)’ in the origin field', () => {
        // @ts-ignore
        expect(homePageObj.getOrigin()).toEqual('London (LON)');
    });
    it('Should display ‘New York (NYC)’ in the destination field.', () => {
        // @ts-ignore
        expect(homePageObj.getDestination()).toEqual('New York (NYC)');
    });
    it('Should display ‘Sat 8/24’ in the departure date field', () => {
        // @ts-ignore
        expect(homePageObj.getDepartureDate()).toBe('Sat 8/24');
    });
    it('Should display ‘Sun 9/22’ in the return date field.', () => {
        // @ts-ignore
        expect(homePageObj.getReturnDate()).toBe('Sun 9/22');
    });
    it('Should display ‘1 Adult, Economy’ in travelers field', () => {
        // @ts-ignore
        expect(homePageObj.getTravelers()).toBe('1 Adult, Economy');
    });
    it('Should display ‘Estimated Price Graph’ below the search form', () => {
        // @ts-ignore
        expect(homePageObj.isGraphVisible()).toEqual(true);
    });
    it('Should display first half of estimated price graph', () => __awaiter(this, void 0, void 0, function* () {
        homePageObj.selectTripType('One-way');
        // @ts-ignore
        expect(homePageObj.getMainVisibleGraphCount('first_half')).toEqual(1);
    }));
    it('Should display both graphs', () => __awaiter(this, void 0, void 0, function* () {
        homePageObj.selectTripType('Round-trip');
        homePageObj.selectDateFromCalendar();
        // @ts-ignore
        expect(homePageObj.getMainVisibleGraphCount('both')).toEqual(2);
    }));
    it('Should display tooltip with price', () => {
        expect(homePageObj.getGraphBarTooltipText()).toContain('USD');
    });
    it('Should highlight selected bar', () => __awaiter(this, void 0, void 0, function* () {
        SELECTED_DATE = yield homePageObj.getNewDate();
        const newSelectGraphBar = yield homePageObj.getNewSelectedGraphBar(SELECTED_DATE);
        expect(homePageObj.getSelectedBarStatus(newSelectGraphBar)).toContain('selected');
    }));
    it('Should display Price of selected bar', () => __awaiter(this, void 0, void 0, function* () {
        const selectedBarStatus = yield homePageObj.isSelectedBarPriceVisible();
        expect(selectedBarStatus).toEqual(true);
    }));
    it('Should display ‘Price shown are estimates per person”', () => {
        const selectedPriceTextShownStatus = homePageObj.isSelectedPriceLabelVisible();
        // @ts-ignore
        expect(selectedPriceTextShownStatus).toEqual(true);
    });
    it('Should display ‘Search these days’ button', () => {
        const searchBtnShown = homePageObj.isSearchBtnVisible();
        // @ts-ignore
        expect(searchBtnShown).toEqual(true);
    });
    it('Should display updated date in first result’s details section', () => __awaiter(this, void 0, void 0, function* () {
        homePageObj.searchTheseDays();
        homePageObj.showDetails();
        const FirstResultDepartureDate = homePageObj.getDepartureDateFromDetailsPanel();
        const expectedDate = moment_1.default(SELECTED_DATE).format('ddd, MMM D');
        // @ts-ignore
        expect(FirstResultDepartureDate).toEqual(expectedDate);
    }));
    it('Should display updated departure date', () => {
        const departureField = homePageObj.getDepartureDate();
        const expectedDate = moment_1.default(SELECTED_DATE).format('ddd M/D');
        // @ts-ignore
        expect(departureField.getText()).toBe(expectedDate);
    });
    it('Should not display ‘Price shown are estimates per person’ label', () => {
        expect(homePageObj.isPricesShownLabelVisible());
    });
    it('Should not display ‘Search these days’ button', () => {
        expect(homePageObj.isSearchTheseDaysBtnVisible());
    });
});
