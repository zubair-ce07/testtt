requirejs(['jquery', 'knockout', 'ko-prerendered', 'ko-contenteditable'], function($, ko){
	var service = function(){
		this.icon = ko.observable('');
		this.serviceID = ko.observable('');
		this.iconId = ko.computed(function () {
	    return this.icon().toString().split(" ")[1];
		}, this);

		this.heading = {
			value : ko.observable(),
			edit : ko.observable(false)
		},
		this.description = {
			value : ko.observable(),	
			edit : ko.observable(false)
		},
		this.iconChange = function(a, selected){
			this.icon("fa "+selected.icon)
		}
		
	}
	var profile = {

		edit: ko.observable(false),
		heading : {
			value : ko.observable(),
			edit : ko.observable(false)
		},
		description : {
			value : ko.observable(),
			edit : ko.observable(false)
		},
		services : ko.observableArray(),
		createService : function() {
		    return new service();
		},
		toggleEdit:function(item){
			item.edit(!item.edit());
			$(".profile_form").submit();
			$(".service_form").submit();
		}
	}
	requirejs(['icon-picker'], function(){
		$("[data-iconpicker]").on("click", function(){
			$('.icp-auto').iconPicker();
		});
	})
	ko.applyBindings(profile);
});