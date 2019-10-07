import axios from 'axios';
import { browser, ElementFinder, ExpectedConditions as EC } from "protractor";

export async function findCurrentLocation(): Promise<string> {
  const response = await axios.get('http://ip-api.com/json');
  const { city, country } = response.data;
  return [city, country].join(', ');
}

export function diffInDays(d1: string, d2: string): number {
  const ONE_DAY_IN_MS = 24 * 60 * 60 * 1000;
  return (toDate(d2).getTime() - toDate(d1).getTime()) / ONE_DAY_IN_MS;
}

export function toDate(text: string): Date {
  const [month, date] = text.split(' ')[1].split('/').map(Number);
  return new Date(new Date().getFullYear(), month - 1, date);
}

export async function waitUntilInteractive(element: ElementFinder, timeout?: number, message?: string): Promise<void> {
  return browser.wait(
    EC.and(
      EC.presenceOf(element),
      EC.visibilityOf(element),
      EC.elementToBeClickable(element)
    ),
    timeout,
    message,
  )
}

export async function makeInteractive(element: ElementFinder): Promise<void> {
  const isDisplayed = await element.isDisplayed();
  
  if (!isDisplayed) {
    scrollIntoView(element);
  }
  
  await waitUntilInteractive(element);
}

export async function click(element: ElementFinder): Promise<void> {
  await makeInteractive(element);
  await element.click();
}

export function scrollIntoView(element: ElementFinder): void {
  browser.executeScript((element: HTMLElement) => element.scrollIntoView(false), element)
}

export async function switchToNewTabIfOpened(act: () => Promise<void>) {
  const windowsBefore = await browser.getAllWindowHandles();
  await act();
  const windowsAfter = await browser.getAllWindowHandles();
  if (windowsBefore.length < windowsAfter.length) {
    await browser.switchTo().window(windowsAfter[windowsAfter.length - 1]);
  }
}
