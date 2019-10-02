"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const protractor_1 = require("protractor");
class FlightsPageObject {
    constructor() {
        this.departureField = protractor_1.element(protractor_1.by.css('div[id$="origin-airport-display"]'));
        this.returnField = protractor_1.element(protractor_1.by.css('div[id$="destination-airport-display"]'));
        this.departureDateText = protractor_1.element(protractor_1.by.css("div[id$='dateRangeInput-display-start']"));
        this.returnDateText = protractor_1.element(protractor_1.by.css("div[id$='dateRangeInput-display-end']"));
        this.cheapestPrice = protractor_1.element(protractor_1.by.css("a[id$='price_aTab']"));
        this.bestPrice = protractor_1.element(protractor_1.by.css("a[id$='bestflight_aTab']"));
        this.quickestPrice = protractor_1.element(protractor_1.by.css("a[id$='duration_aTab']"));
        this.cheapestTime = protractor_1.element(protractor_1.by.css("a[id$='price_aTab'] .js-duration"));
        this.bestTime = protractor_1.element(protractor_1.by.css("a[id$='bestflight_aTab'] .js-duration"));
        this.quickestTime = protractor_1.element(protractor_1.by.css("a[id$='duration_aTab'] .js-duration"));
    }
    getDeparture() {
        return __awaiter(this, void 0, void 0, function* () {
            return yield this.departureField.getText();
        });
    }
    getDestination() {
        return __awaiter(this, void 0, void 0, function* () {
            return yield this.returnField.getText();
        });
    }
    getDepartureDate() {
        return this.departureDateText.getText();
    }
    getReturnDate() {
        return this.returnDateText.getText();
    }
    getTripDates(tripDaysNumber) {
        const todaysDate = new Date();
        const weekdays = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
        todaysDate.setDate(todaysDate.getDate() + tripDaysNumber);
        const departureDayName = weekdays[todaysDate.getDay()];
        return (departureDayName + " " + (todaysDate.getMonth() + 1) + "/" + (todaysDate.getDate()));
    }
    getCheapestPrice() {
        return __awaiter(this, void 0, void 0, function* () {
            return this.getPrice(yield this.cheapestPrice.getText());
        });
    }
    getBestPrice() {
        return __awaiter(this, void 0, void 0, function* () {
            return this.getPrice(yield this.bestPrice.getText());
        });
    }
    getQuickestPrice() {
        return __awaiter(this, void 0, void 0, function* () {
            return this.getPrice(yield this.quickestPrice.getText());
        });
    }
    getPrice(element) {
        return parseFloat(element.match(/\$((?:\d|\,)*\.?\d+)/g)[0].split("$")[1]);
    }
    getCheapestTime() {
        return __awaiter(this, void 0, void 0, function* () {
            return this.getTime(yield this.cheapestTime.getText());
        });
    }
    getBestTime() {
        return __awaiter(this, void 0, void 0, function* () {
            return this.getTime(yield this.bestTime.getText());
        });
    }
    getQuickestTime() {
        return __awaiter(this, void 0, void 0, function* () {
            return this.getTime(yield this.quickestTime.getText());
        });
    }
    getTime(time) {
        const splitTime = time.replace("h", "").replace("m", "").split(" ");
        const timeInMiliSeconds = Number(splitTime[0]) * 3600 + Number(splitTime[1]) * 60;
        return timeInMiliSeconds;
    }
}
exports.FlightsPageObject = FlightsPageObject;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiZmxpZ2h0c1BhZ2VPYmplY3QuanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlcyI6WyIuLi9mbGlnaHRzUGFnZU9iamVjdC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7OztBQUFBLDJDQUFxSDtBQUVySCxNQUFhLGlCQUFpQjtJQUE5QjtRQUNFLG1CQUFjLEdBQWtCLG9CQUFPLENBQUMsZUFBRSxDQUFDLEdBQUcsQ0FBQyxtQ0FBbUMsQ0FBQyxDQUFDLENBQUM7UUFDckYsZ0JBQVcsR0FBa0Isb0JBQU8sQ0FBQyxlQUFFLENBQUMsR0FBRyxDQUFDLHdDQUF3QyxDQUFDLENBQUMsQ0FBQztRQUN2RixzQkFBaUIsR0FBa0Isb0JBQU8sQ0FBQyxlQUFFLENBQUMsR0FBRyxDQUFDLHlDQUF5QyxDQUFDLENBQUMsQ0FBQztRQUM5RixtQkFBYyxHQUFrQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMsdUNBQXVDLENBQUMsQ0FBQyxDQUFDO1FBQ3pGLGtCQUFhLEdBQWtCLG9CQUFPLENBQUMsZUFBRSxDQUFDLEdBQUcsQ0FBQyxxQkFBcUIsQ0FBQyxDQUFDLENBQUM7UUFDdEUsY0FBUyxHQUFrQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMsMEJBQTBCLENBQUMsQ0FBQyxDQUFDO1FBQ3ZFLGtCQUFhLEdBQWtCLG9CQUFPLENBQUMsZUFBRSxDQUFDLEdBQUcsQ0FBQyx3QkFBd0IsQ0FBQyxDQUFDLENBQUM7UUFDekUsaUJBQVksR0FBa0Isb0JBQU8sQ0FBQyxlQUFFLENBQUMsR0FBRyxDQUFDLGtDQUFrQyxDQUFDLENBQUMsQ0FBQztRQUNsRixhQUFRLEdBQWtCLG9CQUFPLENBQUMsZUFBRSxDQUFDLEdBQUcsQ0FBQyx1Q0FBdUMsQ0FBQyxDQUFDLENBQUM7UUFDbkYsaUJBQVksR0FBa0Isb0JBQU8sQ0FBQyxlQUFFLENBQUMsR0FBRyxDQUFDLHFDQUFxQyxDQUFDLENBQUMsQ0FBQztJQTJEdkYsQ0FBQztJQXpETyxZQUFZOztZ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