import { browser, protractor, ElementFinder } from 'protractor';

export async function browserWaitHandler ( ele : ElementFinder) : Promise<void> {
    const expectedCondition = protractor.ExpectedConditions;
    const clickable = expectedCondition.elementToBeClickable(ele);
    browser.wait(clickable, 50000 , 'Message: took too long');
  }