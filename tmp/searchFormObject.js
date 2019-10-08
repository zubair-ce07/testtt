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
class SearchFormObject {
    constructor() {
        this.departureDateField = protractor_1.element.all(protractor_1.by.css('div[id$=dateRangeInput-display-start]')).first();
        this.returnDateField = protractor_1.element.all(protractor_1.by.css('div[id$=dateRangeInput-display-end]')).first();
        this.departureField = protractor_1.element.all(protractor_1.by.css('div[id$="origin-airport-display"]')).first();
        this.destinationField = protractor_1.element(protractor_1.by.css('div[id$="destination-airport-display"]'));
        this.departureDateText = protractor_1.element(protractor_1.by.css("div[id$='dateRangeInput-display-start']"));
    }
    getDepartureText() {
        return __awaiter(this, void 0, void 0, function* () {
            return yield this.departureField.getText();
        });
    }
    getDestinationText() {
        return __awaiter(this, void 0, void 0, function* () {
            return yield this.destinationField.getText();
        });
    }
    getDepartureDateText() {
        return this.departureDateText.getText();
    }
    getReturnDateText() {
        return this.returnDateField.getText();
    }
    getDepartureDisplay() {
        return __awaiter(this, void 0, void 0, function* () {
            return yield this.departureField.isDisplayed();
        });
    }
    getDestinationDisplay() {
        return __awaiter(this, void 0, void 0, function* () {
            return yield this.destinationField.isDisplayed();
        });
    }
    departureDateFieldDisplay() {
        return __awaiter(this, void 0, void 0, function* () {
            return yield this.departureDateField.isDisplayed();
        });
    }
    returnDateFieldDisplay() {
        return __awaiter(this, void 0, void 0, function* () {
            return yield this.returnDateField.isDisplayed();
        });
    }
    waitUntillElementAppears(element) {
        return __awaiter(this, void 0, void 0, function* () {
            let until = yield protractor_1.protractor.ExpectedConditions;
            yield protractor_1.browser.wait(until.visibilityOf(element), 40000, `${element} not appeared in expected time`);
        });
    }
    waitUntillElementDisappear(element) {
        return __awaiter(this, void 0, void 0, function* () {
            let until = yield protractor_1.protractor.ExpectedConditions;
            yield protractor_1.browser.wait(until.invisibilityOf(element), 40000, `${element} not disappeared in expected time`);
        });
    }
}
exports.SearchFormObject = SearchFormObject;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoic2VhcmNoRm9ybU9iamVjdC5qcyIsInNvdXJjZVJvb3QiOiIiLCJzb3VyY2VzIjpbIi4uL3NlYXJjaEZvcm1PYmplY3QudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7QUFBQSwyQ0FBeUk7QUFFekksTUFBYSxnQkFBZ0I7SUFBN0I7UUFDRSx1QkFBa0IsR0FBa0Isb0JBQU8sQ0FBQyxHQUFHLENBQUMsZUFBRSxDQUFDLEdBQUcsQ0FBQyx1Q0FBdUMsQ0FBQyxDQUFDLENBQUMsS0FBSyxFQUFFLENBQUM7UUFDekcsb0JBQWUsR0FBa0Isb0JBQU8sQ0FBQyxHQUFHLENBQUMsZUFBRSxDQUFDLEdBQUcsQ0FBQyxxQ0FBcUMsQ0FBQyxDQUFDLENBQUMsS0FBSyxFQUFFLENBQUM7UUFDcEcsbUJBQWMsR0FBa0Isb0JBQU8sQ0FBQyxHQUFHLENBQUMsZUFBRSxDQUFDLEdBQUcsQ0FBQyxtQ0FBbUMsQ0FBQyxDQUFDLENBQUMsS0FBSyxFQUFFLENBQUM7UUFDakcscUJBQWdCLEdBQWtCLG9CQUFPLENBQUMsZUFBRSxDQUFDLEdBQUcsQ0FBQyx3Q0FBd0MsQ0FBQyxDQUFDLENBQUM7UUFDNUYsc0JBQWlCLEdBQWtCLG9CQUFPLENBQUMsZUFBRSxDQUFDLEdBQUcsQ0FBQyx5Q0FBeUMsQ0FBQyxDQUFDLENBQUM7SUErQ2hHLENBQUM7SUE3Q08sZ0JBQWdCOztZQUNwQixPQUFPLE1BQU0sSUFBSSxDQUFDLGNBQWMsQ0FBQyxPQUFPLEVBQUUsQ0FBQztRQUM3QyxDQUFDO0tBQUE7SUFFSyxrQkFBa0I7O1lBQ3RCLE9BQU8sTUFBTSxJQUFJLENBQUMsZ0JBQWdCLENBQUMsT0FBTyxFQUFFLENBQUM7UUFDL0MsQ0FBQztLQUFBO0lBRUQsb0JBQW9CO1FBQ2xCLE9BQU8sSUFBSSxDQUFDLGlCQUFpQixDQUFDLE9BQU8sRUFBRSxDQUFDO0lBQzFDLENBQUM7SUFFRCxpQkFBaUI7UUFDZixPQUFPLElBQUksQ0FBQyxlQUFlLENBQUMsT0FBTyxFQUFFLENBQUM7SUFDeEMsQ0FBQztJQUVLLG1CQUFtQjs7WUFDeEIsT0FBTyxNQUFNLElBQUksQ0FBQyxjQUFjLENBQUMsV0FBVyxFQUFFLENBQUM7UUFDaEQsQ0FBQztLQUFBO0lBRUsscUJBQXFCOztZQUMxQixPQUFPLE1BQU0sSUFBSSxDQUFDLGdCQUFnQixDQUFDLFdBQVcsRUFBRSxDQUFDO1FBQ25ELENBQUM7S0FBQTtJQUVLLHlCQUF5Qjs7WUFDN0IsT0FBTyxNQUFNLElBQUksQ0FBQyxrQkFBa0IsQ0FBQyxXQUFXLEVBQUUsQ0FBQztRQUNyRCxDQUFDO0tBQUE7SUFFSyxzQkFBc0I7O1lBQzFCLE9BQU8sTUFBTSxJQUFJLENBQUMsZUFBZSxDQUFDLFdBQVcsRUFBRSxDQUFDO1FBQ2xELENBQUM7S0FBQTtJQUVNLHdCQUF3QixDQUFDLE9BQVk7O1lBQ3pDLElBQUksS0FBSyxHQUFpQyxNQUFNLHVCQUFVLENBQUMsa0JBQWtCLENBQUM7WUFDOUUsTUFBTSxvQkFBTyxDQUFDLElBQUksQ0FDbEIsS0FBSyxDQUFDLFlBQVksQ0FBQyxPQUFPLENBQUMsRUFDM0IsS0FBSyxFQUFFLEdBQUcsT0FBTyxnQ0FBZ0MsQ0FBQyxDQUFBO1FBQ3BELENBQUM7S0FBQTtJQUVLLDBCQUEwQixDQUFDLE9BQVk7O1lBQzNDLElBQUksS0FBSyxHQUFpQyxNQUFNLHVCQUFVLENBQUMsa0JBQWtCLENBQUM7WUFDOUUsTUFBTSxvQkFBTyxDQUFDLElBQUksQ0FDbEIsS0FBSyxDQUFDLGNBQWMsQ0FBQyxPQUFPLENBQUMsRUFDN0IsS0FBSyxFQUFFLEdBQUcsT0FBTyxtQ0FBbUMsQ0FBQyxDQUFBO1FBQ3ZELENBQUM7S0FBQTtDQUNGO0FBcERELDRDQW9EQyJ9