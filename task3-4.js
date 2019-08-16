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
	
  	it('should display hotel details and map: Step 3-4', function() {

  		openLink('Hotels');

  		var originField = element.all(by.css("[id *= location-display]")).first().click()
  		browser.wait(EC.visibilityOf(originField),7000);
  		//set the origin

		var originText = element.all(by.css("[id *= textInputWrapper]")).first().element(by.tagName('input'));
		browser.wait(EC.visibilityOf(originText),7000);
		originText.sendKeys("BCN");
		//select the origin

  		var originList = element.all(by.css("[id *= location-smarty-content]")).first();

  		expect((originList).isPresent()).toBe(true);
  		
  		browser.wait(EC.elementToBeClickable(originList),5000);

  		originList.all(by.tagName('li')).first().click();

  		//press the search button

  		var searchBtn = element(by.css("[id$=-formGridSearchBtn]")).element(by.tagName('button'));
  		searchBtn.click().then( function() {

  			// check the result set
	  		var resultsContainer = element(by.css("[id = searchResultsList]"));
	  		browser.wait(EC.presenceOf(resultsContainer),10000);
			
			var resultbox = element(by.css("[class *= normalResults]"));
			browser.wait(EC.presenceOf(resultbox),10000);

			var results = resultsContainer.all(by.css("[class*=Base-Results-HorizonResult]"));
			browser.wait(EC.presenceOf(results),10000);

			// select hotel and check
			var hotel = results.first();
			// click the first option

			hotel.click().then( function() {

				//check the details section

				var detailsCon = element.all(by.css("[id*=detailsWrapper]")).first();
				browser.wait(EC.visibilityOf(detailsCon),6000);

				expect((detailsCon).isPresent()).toBe(true);

				//check the photos section

				var photosCon = element.all(by.css("[class*=col-photos]")).first();
				browser.wait(EC.visibilityOf(photosCon),7000);

				expect((photosCon).isPresent()).toBe(true);

				//Step 4: check the map in map tab

				var mapTab = detailsCon.all(by.css("[id*=map]")).first();
				browser.wait(EC.presenceOf(mapTab),7000);

				expect((mapTab).isPresent()).toBe(true);

				mapTab.click().then(function(){

					var mapContainer = element.all(by.css("[id*=mapContainer]")).first();
					browser.wait(EC.visibilityOf(mapContainer),15000);

					var map = mapContainer.all(by.css("[class*=gm-style]")).first();
					browser.wait(EC.visibilityOf(map),10000);

					expect((map).isPresent()).toBe(true);


				});
				
			});			
		});

  	});	
  	
});
