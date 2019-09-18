import { browser, ElementFinder } from "protractor";

export async function scrollElementIntoView(elm: ElementFinder): Promise<void> {
  return browser.executeScript((elm: HTMLElement) => elm.scrollIntoView(false), elm);
}
