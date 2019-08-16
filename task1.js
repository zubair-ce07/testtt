// testcases.js
describe('kayak website', function() {
	beforeEach (function(){
		browser.waitForAngularEnabled(false);
		browser.get('https://www.kayak.com/');
		global.EC = protractor.ExpectedConditions;

	});

	function openLink(link){
		var link = element(by.linkText(link));
    	browser.wait(EC.visibilityOf(link),15000);
    	link.click();
	}
	
	
  	it('should check the link title and fields: Step 1', function() {
    	
		openLink('Hotels');

		// Check Title of the page
    	expect(browser.getTitle()).toEqual(browser.params.hotleLinkTitle);

    	//Check the guests field is displayed or not

    	var guestField = element(by.css("[id *= roomsGuestsAboveForm]")).element(by.css("[class *= _idj]"));

    	expect(guestField.getText()).toBe('1 room, 2 guests');

    	//Check the origin field is displayed or not

    	var originField = element(by.css("[id *= location-textInputWrapper]"));

  		expect((originField).isPresent()).toBe(true);

  		//Check the start date field is displayed or not

  		var startDateField = element(by.css("[id *= dateRangeInput-display-start]"));

  		expect((startDateField).isPresent()).toBe(true);

  		//Check the end date field is displayed or not

  		var endDateField = element(by.css("[id *= dateRangeInput-display-end]"));

  		expect((endDateField).isPresent()).toBe(true);

   
  	}); 
	
  	
});
