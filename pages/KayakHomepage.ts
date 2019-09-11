import {browser, by, element, ElementFinder} from "protractor";
import CommonHelper from "../helper/CommonHelper";

export default class KayakHomepage {
    commonHelperObj = new CommonHelper();
    tripsPageBtn: ElementFinder = element(by.css("a[id*='-trips-button']"));
    signInBtn: ElementFinder = element(by.css("button[id*='account-button']"));
    signInDropdown: ElementFinder = element(by.css("div[id*='-accountDropdown-dropdown-inner']"));
    emailInputBox: ElementFinder = element(by.css("input[id*='-username']"));
    passwordInputBox: ElementFinder = element(by.css("input[id*='-password']"));
    submitBtn: ElementFinder = this.signInDropdown.element(by.css('.Common-Widgets-Button-StyleJamButton'));
    myAccountBtn: ElementFinder = element(by.css("div[id*='-account-link']"));

    async goToTripsPage(): Promise<void> {
       await this.tripsPageBtn.click();
    }
    async getSignInDropdown(): Promise<void> {
        await this.signInBtn.click();
        await this.commonHelperObj.waitForElementToBeVisible(this.emailInputBox);
    }
    async signInUsingCred(): Promise<void> {
        await this.emailInputBox.sendKeys(this.commonHelperObj.email);
        await this.passwordInputBox.sendKeys(this.commonHelperObj.password);
        await this.submitBtn.click();
    }
    async isUserSignedIn(): Promise<boolean> {
        await this.commonHelperObj.waitForElementToBeVisible(this.myAccountBtn);
        return await this.myAccountBtn.isDisplayed();
    }
}