import { browser } from 'protractor';
import { expect } from 'chai';

describe('kayak.com/flights', () => {
  
  it('should be able to load Flight Front Door', async () => {
    const url = 'https://www.kayak.com/flights';
    await browser.get(url);
    expect(await browser.getCurrentUrl()).equal(url);
  });
  
  it('should be able to tap on Multi city tab', async () => {
  
  });
  
  it('should show 2 legs by default', async () => {
  
  });
  
  it('should show Origin Selector on leg 1', async () => {
  
  });
  
  it('should show Destination Selector on leg 1', async () => {
  
  });
  
  it('should show Date Picker on leg 1', async () => {
  
  });
  
  it('should be able to tap on the Add button', async () => {
  
  });
  
  it('should add another leg (Origin, destination and Date picker)', async () => {
  
  });
  
  it('should be able to tap 5 times on the Add button', async () => {
  
  });
  
  it('should add 3 more legs (6 legs is the maximum)', async () => {
  
  });
  
  it('should be able to tap on the Remove button', async () => {
  
  });
  
  it('should remove the last leg', async () => {
  
  });
  
  it('should be able to tap on the Add button', async () => {
  
  });
  
  [
    { origin: 'BOS', destination: 'MIA', date: 7, },
    { origin: 'MIA', destination: 'LAX', date: 14, },
    { origin: 'LAX', destination: 'CHI', date: 21, },
    { origin: 'CHI', destination: 'NYC', date: 28, },
    { origin: 'NYC', destination: 'DFW', date: 35, },
    { origin: 'DFW', destination: 'WAS', date: 42, },
  ].forEach((leg, index) => {
    it(`should set leg: ${index + 1} origin as ${leg.origin}`, async () => {
    
    });
    
    it(`should set leg: ${index + 1} destination as ${leg.destination}`, async () => {
    
    });
    
    it(`should set leg: ${index + 1} date as {Today+${leg.date}}`, async () => {
    
    });
  });
  
  it('should be able to tap on the search CTA', async () => {
  
  });
  
  it('should show {BOS} - {WAS}, {Today+7} - {Today+42}, {1} traveller in the FRP header', async () => {
  
  });
  
  it('should wait for the search to complete', async () => {
  
  });
  
  it('should go back to the front door and remove the last leg if no results show up (fail the test if no results show up for a 3 leg search)', async () => {
  
  });
  
  it('should show Airline name/logo on all legs on any flight card', async () => {
  
  });
  
  it('should show departure and arrival Times on all legs on any flight card', async () => {
  
  });
  
  it('should show departure and arrival Airport Codes for all legs on any flight card', async () => {
  
  });
  
  it('should show Duration for all legs on any flight card', async () => {
  
  });
  
  it('should show Price on any flight card', async () => {
  
  });
  
  it('should be able to tap on any non-hacker fare flight card', async () => {
  
  });
  
  it('should show matching departure and arrival airport codes in the Flight Detail Page (same as FRP)', async () => {
  
  });
  
  it('should show {Today+7} as departure date and  {Today+42} as return date in the FDP', async () => {
  
  });
  
  it('should show {1} Traveller in the FDP', async () => {
  
  });
  
  it('should show matching Airline name/logo on the FDP (same as FRP)', async () => {
  
  });
  
  it('should show same cheapest Price on FDP as the Price on FRP', async () => {
  
  });
  
  it('should show matching departure and arrival Times for all legs on the FDP (same as FRP)', async () => {
  
  });
  
  it('should show matching Duration for all legs on the FDP (same as FRP)', async () => {
  
  });
  
  it('should show flight # on each leg in the FDP', async () => {
  
  });
  
  it('should show cabin class on each leg in the FDP', async () => {
  
  });
});
