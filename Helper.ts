import {browser, $, element, by, protractor, promise} from 'protractor';
export class Helper {

    getDate(numberOfDaysToBeAdded: number): string {
        const departureDate: Date = new Date();
        departureDate.setDate(departureDate.getDate() + numberOfDaysToBeAdded); 
        const monthNames: Array<string> = ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"];
        let currentDate: string = departureDate.getDate().toString();
        let currentMonth: string =monthNames[departureDate.getMonth()];
        return (`${currentMonth} ${currentDate}`);
    }

    getKayakFormatedDate(numberOfDaysToBeAdded: number): string {
        const departureDate = new Date();
        departureDate.setDate(departureDate.getDate() + numberOfDaysToBeAdded);
        const weekdays: Array<string> = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
        const departureDayName: string = weekdays[departureDate.getDay()];
        return (`${departureDayName} ${departureDate.getMonth() + 1}/${departureDate.getDate()}`);
    }

    getSwissFormatedDate(numberOfDaysToBeAdded: number): string {
        const departureDate = new Date();
        departureDate.setDate(departureDate.getDate() + numberOfDaysToBeAdded);
        let currentDate: string = departureDate.getDate().toString();
        let currentMonth: string = (departureDate.getMonth() + 1).toString();
        let currentYear: string = departureDate.getFullYear().toString();
        if(departureDate.getDate() < 10) {
            currentDate = "0" + currentDate;
        }
        if(departureDate.getMonth() < 10) {
            currentMonth = "0" + currentMonth;
        }
        return (`${currentMonth}/${currentDate}/${currentYear}`);
    }

}