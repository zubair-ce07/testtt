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
        this.cheapestPrice = protractor_1.element(protractor_1.by.css("a[id$='price_aTab']"));
        this.bestPrice = protractor_1.element(protractor_1.by.css("a[id$='bestflight_aTab']"));
        this.quickestPrice = protractor_1.element(protractor_1.by.css("a[id$='duration_aTab']"));
        this.cheapestTime = protractor_1.element(protractor_1.by.css("a[id$='price_aTab'] .js-duration"));
        this.bestTime = protractor_1.element(protractor_1.by.css("a[id$='bestflight_aTab'] .js-duration"));
        this.quickestTime = protractor_1.element(protractor_1.by.css("a[id$='duration_aTab'] .js-duration"));
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
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiZmxpZ2h0c1BhZ2VPYmplY3QuanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlcyI6WyIuLi9mbGlnaHRzUGFnZU9iamVjdC50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOzs7Ozs7Ozs7OztBQUFBLDJDQUFxSDtBQUVySCxNQUFhLGlCQUFpQjtJQUE5QjtRQUNFLGtCQUFhLEdBQWtCLG9CQUFPLENBQUMsZUFBRSxDQUFDLEdBQUcsQ0FBQyxxQkFBcUIsQ0FBQyxDQUFDLENBQUM7UUFDdEUsY0FBUyxHQUFrQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMsMEJBQTBCLENBQUMsQ0FBQyxDQUFDO1FBQ3ZFLGtCQUFhLEdBQWtCLG9CQUFPLENBQUMsZUFBRSxDQUFDLEdBQUcsQ0FBQyx3QkFBd0IsQ0FBQyxDQUFDLENBQUM7UUFDekUsaUJBQVksR0FBa0Isb0JBQU8sQ0FBQyxlQUFFLENBQUMsR0FBRyxDQUFDLGtDQUFrQyxDQUFDLENBQUMsQ0FBQztRQUNsRixhQUFRLEdBQWtCLG9CQUFPLENBQUMsZUFBRSxDQUFDLEdBQUcsQ0FBQyx1Q0FBdUMsQ0FBQyxDQUFDLENBQUM7UUFDbkYsaUJBQVksR0FBa0Isb0JBQU8sQ0FBQyxlQUFFLENBQUMsR0FBRyxDQUFDLHFDQUFxQyxDQUFDLENBQUMsQ0FBQztJQTJDdkYsQ0FBQztJQXpDQyxZQUFZLENBQUMsY0FBc0I7UUFDakMsTUFBTSxVQUFVLEdBQUcsSUFBSSxJQUFJLEVBQUUsQ0FBQztRQUM5QixNQUFNLFFBQVEsR0FBa0IsQ0FBQyxLQUFLLEVBQUUsS0FBSyxFQUFFLEtBQUssRUFBRSxLQUFLLEVBQUUsS0FBSyxFQUFFLEtBQUssRUFBRSxLQUFLLENBQUMsQ0FBQztRQUNsRixVQUFVLENBQUMsT0FBTyxDQUFDLFVBQVUsQ0FBQyxPQUFPLEVBQUUsR0FBRyxjQUFjLENBQUMsQ0FBQztRQUMxRCxNQUFNLGdCQUFnQixHQUFHLFFBQVEsQ0FBQyxVQUFVLENBQUMsTUFBTSxFQUFFLENBQUMsQ0FBQztRQUN2RCxPQUFPLENBQUMsZ0JBQWdCLEdBQUcsR0FBRyxHQUFHLENBQUMsVUFBVSxDQUFDLFFBQVEsRUFBRSxHQUFHLENBQUMsQ0FBQyxHQUFHLEdBQUcsR0FBRyxDQUFDLFVBQVUsQ0FBQyxPQUFPLEVBQUUsQ0FBQyxDQUFDLENBQUM7SUFDL0YsQ0FBQztJQUVLLGdCQUFnQjs7WUFDcEIsT0FBTyxJQUFJLENBQUMsUUFBUSxDQUFDLE1BQU0sSUFBSSxDQUFDLGFBQWEsQ0FBQyxPQUFPLEVBQUUsQ0FBQyxDQUFDO1FBQzNELENBQUM7S0FBQTtJQUVLLFlBQVk7O1lBQ2hCLE9BQU8sSUFBSSxDQUFDLFFBQVEsQ0FBQyxNQUFNLElBQUksQ0FBQyxTQUFTLENBQUMsT0FBTyxFQUFFLENBQUMsQ0FBQztRQUN2RCxDQUFDO0tBQUE7SUFFSyxnQkFBZ0I7O1lBQ3BCLE9BQU8sSUFBSSxDQUFDLFFBQVEsQ0FBQyxNQUFNLElBQUksQ0FBQyxhQUFhLENBQUMsT0FBTyxFQUFFLENBQUMsQ0FBQztRQUMzRCxDQUFDO0tBQUE7SUFFRCxRQUFRLENBQUMsT0FBZTtRQUN0QixPQUFPLFVBQVUsQ0FBQyxPQUFPLENBQUMsS0FBSyxDQUFDLHVCQUF1QixDQUFDLENBQUMsQ0FBQyxDQUFDLENBQUMsS0FBSyxDQUFDLEdBQUcsQ0FBQyxDQUFDLENBQUMsQ0FBQyxDQUFDLENBQUM7SUFDN0UsQ0FBQztJQUVLLGVBQWU7O1lBQ25CLE9BQU8sSUFBSSxDQUFDLE9BQU8sQ0FBQyxNQUFNLElBQUksQ0FBQyxZQUFZLENBQUMsT0FBTyxFQUFFLENBQUMsQ0FBQztRQUN6RCxDQUFDO0tBQUE7SUFFSyxXQUFXOztZQUNmLE9BQU8sSUFBSSxDQUFDLE9BQU8sQ0FBQyxNQUFNLElBQUksQ0FBQyxRQUFRLENBQUMsT0FBTyxFQUFFLENBQUMsQ0FBQztRQUNyRCxDQUFDO0tBQUE7SUFFSyxlQUFlOztZQUNuQixPQUFPLElBQUksQ0FBQyxPQUFPLENBQUMsTUFBTSxJQUFJLENBQUMsWUFBWSxDQUFDLE9BQU8sRUFBRSxDQUFDLENBQUM7UUFDekQsQ0FBQztLQUFBO0lBRUQsT0FBTyxDQUFDLElBQUk7UUFDVixNQUFNLFNBQVMsR0FBRyxJQUFJLENBQUMsT0FBTyxDQUFDLEdBQUcsRUFBRSxFQUFFLENBQUMsQ0FBQyxPQUFPLENBQUMsR0FBRyxFQUFFLEVBQUUsQ0FBQyxDQUFDLEtBQUssQ0FBQyxHQUFHLENBQUMsQ0FBQztRQUNwRSxNQUFNLGlCQUFpQixHQUFHLE1BQU0sQ0FBQyxTQUFTLENBQUMsQ0FBQyxDQUFDLENBQUMsR0FBQyxJQUFJLEdBQUcsTUFBTSxDQUFDLFNBQVMsQ0FBQyxDQUFDLENBQUMsQ0FBQyxHQUFDLEVBQUUsQ0FBQztRQUM5RSxPQUFPLGlCQUFpQixDQUFDO0lBQzNCLENBQUM7Q0FDRjtBQWpERCw4Q0FpREMifQ==