"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const commonPage_1 = require("./commonPage");
const FlightResultsPage_1 = require("./FlightResultsPage");
const kayakHelper_1 = require("./kayakHelper");
class kayakFactory {
    constructor() {
        this.createKayakPageObject = function (type) {
            if (type === "commonPage") {
                return new commonPage_1.commonPage();
            }
            else if (type === "flightResultsPage") {
                return new FlightResultsPage_1.FlightResultsPage();
            }
            else if (type === "kayakHelper") {
                return new kayakHelper_1.kayakHelper();
            }
        };
    }
}
exports.kayakFactory = kayakFactory;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoia2F5YWtGYWN0b3J5LmpzIiwic291cmNlUm9vdCI6IiIsInNvdXJjZXMiOlsiLi4va2F5YWtGYWN0b3J5LnRzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiI7O0FBQUEsNkNBQXdDO0FBQ3hDLDJEQUFxRDtBQUNyRCwrQ0FBMEM7QUFFMUM7SUFBQTtRQUNXLDBCQUFxQixHQUFHLFVBQVMsSUFBWTtZQUVoRCxJQUFJLElBQUksS0FBSyxZQUFZLEVBQUU7Z0JBQ3ZCLE9BQU8sSUFBSSx1QkFBVSxFQUFFLENBQUM7YUFDM0I7aUJBQ0ksSUFBSSxJQUFJLEtBQUssbUJBQW1CLEVBQUU7Z0JBQ25DLE9BQU8sSUFBSSxxQ0FBaUIsRUFBRSxDQUFDO2FBQ2xDO2lCQUNJLElBQUksSUFBSSxLQUFLLGFBQWEsRUFBRTtnQkFDN0IsT0FBTyxJQUFJLHlCQUFXLEVBQUUsQ0FBQzthQUM1QjtRQUVMLENBQUMsQ0FBQTtJQUNMLENBQUM7Q0FBQTtBQWRELG9DQWNDIn0=