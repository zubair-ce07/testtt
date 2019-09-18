import { browser, ElementFinder } from "protractor";

export function scrollElementIntoView(elm: ElementFinder) {
  return browser.executeScript((elm: HTMLElement) => elm.scrollIntoView(false), elm);
}
