import {by, element, ElementFinder} from "protractor";

export default class CommonElements {
    hotelsFrontPageLink: ElementFinder = element(by.css("a[href='/hotels']"));
}