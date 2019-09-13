import {by, element} from "protractor";

export default class KayakHomepage {
    carsBtn = element(by.css("li[class*='vertical-cars']"));
    async clickCarsBtn(): Promise<void> {
        await this.carsBtn.click();
    }
}