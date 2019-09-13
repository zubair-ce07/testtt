import {by, element} from "protractor";
import CommonHelper from "../helper/CommonHelper";

export default class KayakHomepage {
    commonHelperObj = new CommonHelper();
    carsBtn = element(by.css("li[class*='vertical-cars']"));
    async clickCarsBtn(): Promise<void> {
        await this.carsBtn.click();
        await this.commonHelperObj.waitForURLToBeLoaded('/cars');
    }
}
