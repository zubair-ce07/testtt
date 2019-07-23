import {browser, $, element, by, protractor, promise} from 'protractor';
export class kayakHelper {

    getPrice(element: string): number {
        return element.match(/\$((?:\d|\,)*\.?\d+)/g) != null ? parseFloat(element.match(/\$((?:\d|\,)*\.?\d+)/g)[0].split("$")[1]) : null;
    }
}