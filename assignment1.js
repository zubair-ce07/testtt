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
    	expect(browser.getTitle()).toEqual('Hotels: Find Cheap Hotel Deals & Discounts - KAYAK');

    	//Check the guests field is displayed or not

    	var guestField = element(by.css("div[id *= roomsGuestsAboveForm]")).element(by.css("div[class *= _idj]"));

    	expect(guestField.getText()).toBe('1 room, 2 guests');

    	//Check the origin field is displayed or not

    	var originField = element(by.css("div[id *= location-textInputWrapper]"));

  		expect((originField).isPresent()).toBe(true);

  		//Check the start date field is displayed or not

  		var startDateField = element(by.css("div[id *= dateRangeInput-display-start]"));

  		expect((startDateField).isPresent()).toBe(true);

  		//Check the end date field is displayed or not

  		var endDateField = element(by.css("div[id *= dateRangeInput-display-end]"));

  		expect((endDateField).isPresent()).toBe(true);

  		console.log("Done With step 1");

   
  	}); 

  	it('should set BCN and search hotels: Step 2-10', function() {

  		openLink('Hotels');

  		browser.sleep(3000);


  		var originField = element.all(by.css("div[id *= location-display]")).first().click()
  		browser.wait(EC.visibilityOf(originField),7000);
  		//set the origin

		var originText = element.all(by.css("div[id *= textInputWrapper]")).first().element(by.tagName('input'));
		browser.wait(EC.visibilityOf(originText),7000);
		originText.sendKeys("BCN");
		browser.sleep(2000);

		//select the origin

  		var originList = element.all(by.css("div[id *= location-smarty-content]")).first();

  		expect((originList).isPresent()).toBe(true);
  		
  		browser.wait(EC.elementToBeClickable(originList),5000);

  		originList.all(by.tagName('li')).first().click();

  		browser.sleep(2000);

  		//press the search button

  		var searchBtn = element(by.css("div[id$=-formGridSearchBtn]")).element(by.tagName('button'));
  		searchBtn.click().then( function() {

  			// check the result set
	  		var resultsContainer = element(by.css("div[id = searchResultsList]"));
	  		browser.wait(EC.presenceOf(resultsContainer),10000);
			
			var resultbox = element(by.css("div[class *= normalResults]"));
			browser.wait(EC.presenceOf(resultbox),10000);

			browser.sleep(5000);

			var results = resultsContainer.all(by.css("div[class*=Base-Results-HorizonResult]"));
			browser.wait(EC.presenceOf(results),10000);

			var resultCount = results.count();

			expect(resultCount).toBeGreaterThanOrEqual(5);

			console.log("Done With step 2");

			
			// select hotel and check
			var hotel = results.first();
			// click the first option

			hotel.click().then( function() {

				//check the details section

				var detailsCon = element.all(by.css("div[id*=detailsWrapper]")).first();
				browser.wait(EC.visibilityOf(detailsCon),6000);

				expect((detailsCon).isPresent()).toBe(true);

				//check the photos section

				var photosCon = element.all(by.css("div[class*=col-photos]")).first();
				browser.wait(EC.visibilityOf(photosCon),7000);

				expect((photosCon).isPresent()).toBe(true);

				console.log("Done With step 3");


				//Step 4: check the map in map tab

				var mapTab = detailsCon.all(by.css("div[id*=map]")).first();
				browser.wait(EC.presenceOf(mapTab),7000);

				expect((mapTab).isPresent()).toBe(true);

				mapTab.click().then(function(){

					var mapContainer = element.all(by.css("div[id*=mapContainer]")).first();
					browser.wait(EC.visibilityOf(mapContainer),15000);

					var map = mapContainer.all(by.css("div[class*=gm-style]")).first();
					browser.wait(EC.visibilityOf(map),10000);

					expect((map).isPresent()).toBe(true);

					console.log("Done With step 4");

				});

				//Step 5: check the reviews in review tab

				var reviewTab = detailsCon.all(by.css("div[id*=reviews]")).first();
				browser.wait(EC.visibilityOf(reviewTab),7500);

				expect((reviewTab).isPresent()).toBe(true);

				reviewTab.click().then(function(){

					var reviewContainer = element.all(by.css("div[id*=reviewsContainer]")).first();
					browser.wait(EC.visibilityOf(reviewContainer),3000);

					expect((reviewContainer).isPresent()).toBe(true);

					console.log("Done With step 5");

				});

				//Step 6: check the rates in rate tab

				var ratesTab = detailsCon.all(by.css("div[id*=rates]")).first();
				browser.wait(EC.visibilityOf(ratesTab),6000);

				expect((ratesTab).isPresent()).toBe(true);

				ratesTab.click().then(function(){

					var ratesContainer = element.all(by.css("div[id*=ratesContainer]")).first();
					browser.wait(EC.visibilityOf(ratesContainer),4000);

					expect((ratesContainer).isPresent()).toBe(true);
					console.log("Done With step 6");

				});	
				
			});

			
			//Step 7: Go to map view

				var mapView = element.all(by.css("div[class *= filterListContainer]")).first();
				
				expect((mapView).isPresent()).toBe(true);
				var mapBtn = mapView.element(by.css(".showMap"));
				expect((mapBtn).isPresent()).toBe(true);
				mapBtn.click().then( function(){

					// check the rail filters

					var mapContainer = element.all(by.css("div[class *= rail-map-container")).first();
					browser.wait(EC.elementToBeClickable(mapContainer),10000);
					expect((mapContainer).isPresent()).toBe(true);

					console.log("Done With step 7");

					//Step 8: mouse hover the hotel markers
					browser.wait(EC.visibilityOf(mapContainer.element(by.css(".gm-style"))),15000);
					var hotelMarker = mapContainer.all(by.css(".hotel-marker"));					
					var selectedHotel = hotelMarker.first();

					hotelMarker.each(function(elem, index) { 


						elem.getCssValue("top").then(function(top){
						
							if(top > 0) {
								selectedHotel = element;
								expect((selectedHotel).isPresent()).toBe(true);	
								browser.actions().mouseMove(selectedHotel).mouseMove(selectedHotel).perform().then(function(){
									
									var hotelId = selectedHotel.getAttribute("id").then(function(value){

										var id = value.substring(value.indexOf('-'), value.length);
										var cardId= 'summaryCard' + id;

										var summaryCard = element(by.css("div[id *= " + cardId + "]"));

										expect((summaryCard).isDisplayed()).toBeTruthy();
										
									});
								
								});	
							}	

						});
					});

					console.log("Done With step 8");

					//Step 9: click the deal btn

					browser.actions().mouseMove(selectedHotel).mouseMove(selectedHotel).click().perform().then( function(){
						var resultWrapper = element.all(by.css("div[class *= resultWrapper]")).first();
						browser.wait(EC.visibilityOf(resultWrapper),10000);

						var itemWrapper = resultWrapper.all(by.css("div[id *= mainItemWrapper]")).first();
						browser.wait(EC.visibilityOf(itemWrapper),10000);

						console.log("Done With step 9");

						var dealBtn = element(by.css("button[id *= bookButton]"));
						dealBtn.click().then(function(){

							// Step 10: check the deals in new tab
							browser.sleep(5000);
							browser.getAllWindowHandles().then(function (handles) {
					            newWindowHandle = handles[1]; // this is your new window
					            browser.switchTo().window(newWindowHandle).then(function () {
					                expect(browser.getCurrentUrl()).toMatch("https://www.hotels.com/"); //someURL
					            });
					        });
						});

						console.log("Done With step 10");

					});
				});
		});

  	});	
  	
});
