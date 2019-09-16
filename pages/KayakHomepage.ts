import {browser, by, element, ElementFinder} from "protractor";
import CommonHelper from "../helper/CommonHelper";

export default class KayakHomepage {
    commonHelperObj = new CommonHelper();

    getTabsBtn(btnType: string): ElementFinder {
        return element(by.css('.TopNavLinks__vertical--'+btnType));
    }
    async isBtnVisible(btnName): Promise<boolean> {
        return await this.getTabsBtn(btnName).isDisplayed();
    }
    async isHighlighted(btnName: string): Promise<boolean> {
        const btn = await this.getTabsBtn(btnName);
        const btnClass = await btn.getAttribute('class');
        return btnClass.includes('active');
    }
    async clickBtn(btn: ElementFinder): Promise<void> {
        const btnClassName = await btn.getAttribute('class');
        await btn.click();
        await this.waitForElementToBeActive(btnClassName);
    }
    async loadPage(pageName: string) {
        const btn = await this.getTabsBtn(pageName);
        await this.clickBtn(btn);
        await this.commonHelperObj.waitForURLToBeLoaded(pageName);
    }
    async waitForElementToBeActive(className: string) {
        await browser.wait(async () => {
            const currentElement = element(by.className(className));
            await this.commonHelperObj.waitForElementToBeVisible(currentElement);
            const attribute = await element(by.className(className)).getAttribute('class');
            return attribute.includes('active');
        }, 5000)
    }
}
