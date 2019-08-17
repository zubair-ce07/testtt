import { browser, protractor, element, by, $$, ElementArrayFinder, ElementFinder } from 'protractor';

export async function browserWaitHandler ( ele : ElementFinder) : Promise<void> {
    const expectedCondition = protractor.ExpectedConditions;
    const clickable = expectedCondition.elementToBeClickable(ele);
    browser.wait(clickable, 5000);
  }
