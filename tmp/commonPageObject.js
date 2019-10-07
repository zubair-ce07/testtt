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
class CommonPageObject {
    constructor() {
        this.departureDateField = protractor_1.element(protractor_1.by.css('div[id$=dateRangeInput-display-start]'));
        this.returnDateField = protractor_1.element(protractor_1.by.css('div[id$=dateRangeInput-display-end]'));
        this.departureField = protractor_1.element.all(protractor_1.by.css('div[id$="origin-airport-display"]')).first();
        this.destinationField = protractor_1.element(protractor_1.by.css('div[id$="destination-airport-display"]'));
        this.departureDateText = protractor_1.element(protractor_1.by.css("div[id$='dateRangeInput-display-start']"));
        this.returnDateText = protractor_1.element(protractor_1.by.css("div[id$='dateRangeInput-display-end']"));
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
        return this.returnDateText.getText();
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
exports.CommonPageObject = CommonPageObject;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiY29tbW9uUGFnZU9iamVjdC5qcyIsInNvdXJjZVJvb3QiOiIiLCJzb3VyY2VzIjpbIi4uL2NvbW1vblBhZ2VPYmplY3QudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7Ozs7QUFBQSwyQ0FBeUk7QUFFekksTUFBYSxnQkFBZ0I7SUFBN0I7UUFDRSx1QkFBa0IsR0FBa0Isb0JBQU8sQ0FBQyxlQUFFLENBQUMsR0FBRyxDQUFDLHVDQUF1QyxDQUFDLENBQUMsQ0FBQztRQUM3RixvQkFBZSxHQUFrQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMscUNBQXFDLENBQUMsQ0FBQyxDQUFDO1FBQ3hGLG1CQUFjLEdBQWtCLG9CQUFPLENBQUMsR0FBRyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMsbUNBQW1DLENBQUMsQ0FBQyxDQUFDLEtBQUssRUFBRSxDQUFDO1FBQ2pHLHFCQUFnQixHQUFrQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMsd0NBQXdDLENBQUMsQ0FBQyxDQUFDO1FBQzVGLHNCQUFpQixHQUFrQixvQkFBTyxDQUFDLGVBQUUsQ0FBQyxHQUFHLENBQUMseUNBQXlDLENBQUMsQ0FBQyxDQUFDO1FBQzlGLG1CQUFjLEdBQWtCLG9CQUFPLENBQUMsZUFBRSxDQUFDLEdBQUcsQ0FBQyx1Q0FBdUMsQ0FBQyxDQUFDLENBQUM7SUErQzNGLENBQUM7SUE3Q08sZ0JBQWdCOztZQUNwQixPQUFPLE1BQU0sSUFBSSxDQUFDLGNBQWMsQ0FBQyxPQUFPLEVBQUUsQ0FBQztRQUM3QyxDQUFDO0tBQUE7SUFFSyxrQkFBa0I7O1lBQ3RCLE9BQU8sTUFBTSxJQUFJLENBQUMsZ0JBQWdCLENBQUMsT0FBTyxFQUFFLENBQUM7UUFDL0MsQ0FBQztLQUFBO0lBRUQsb0JBQW9CO1FBQ2xCLE9BQU8sSUFBSSxDQUFDLGlCQUFpQixDQUFDLE9BQU8sRUFBRSxDQUFDO0lBQzFDLENBQUM7SUFFRCxpQkFBaUI7UUFDZixPQUFPLElBQUksQ0FBQyxjQUFjLENBQUMsT0FBTyxFQUFFLENBQUM7SUFDdkMsQ0FBQztJQUVLLG1CQUFtQjs7WUFDekIsT0FBTyxNQUFNLElBQUksQ0FBQyxjQUFjLENBQUMsV0FBVyxFQUFFLENBQUM7UUFDL0MsQ0FBQztLQUFBO0lBRUsscUJBQXFCOztZQUMzQixPQUFPLE1BQU0sSUFBSSxDQUFDLGdCQUFnQixDQUFDLFdBQVcsRUFBRSxDQUFDO1FBQ2xELENBQUM7S0FBQTtJQUVLLHlCQUF5Qjs7WUFDOUIsT0FBTyxNQUFNLElBQUksQ0FBQyxrQkFBa0IsQ0FBQyxXQUFXLEVBQUUsQ0FBQztRQUNwRCxDQUFDO0tBQUE7SUFFSyxzQkFBc0I7O1lBQzNCLE9BQU8sTUFBTSxJQUFJLENBQUMsZUFBZSxDQUFDLFdBQVcsRUFBRSxDQUFDO1FBQ2pELENBQUM7S0FBQTtJQUVNLHdCQUF3QixDQUFDLE9BQVk7O1lBQ3ZDLElBQUksS0FBSyxHQUFpQyxNQUFNLHVCQUFVLENBQUMsa0JBQWtCLENBQUM7WUFDOUUsTUFBTSxvQkFBTyxDQUFDLElBQUksQ0FDbEIsS0FBSyxDQUFDLFlBQVksQ0FBQyxPQUFPLENBQUMsRUFDM0IsS0FBSyxFQUFFLEdBQUcsT0FBTyxnQ0FBZ0MsQ0FBQyxDQUFBO1FBQ3RELENBQUM7S0FBQTtJQUVLLDBCQUEwQixDQUFDLE9BQVk7O1lBQzNDLElBQUksS0FBSyxHQUFpQyxNQUFNLHVCQUFVLENBQUMsa0JBQWtCLENBQUM7WUFDOUUsTUFBTSxvQkFBTyxDQUFDLElBQUksQ0FDbEIsS0FBSyxDQUFDLGNBQWMsQ0FBQyxPQUFPLENBQUMsRUFDN0IsS0FBSyxFQUFFLEdBQUcsT0FBTyxtQ0FBbUMsQ0FBQyxDQUFBO1FBQ3ZELENBQUM7S0FBQTtDQUNGO0FBckRELDRDQXFEQyJ9