var require = {
	   baseUrl: '/assets', 
       paths: {
        'jquery' : '//cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min',
        'knockout' : '//cdnjs.cloudflare.com/ajax/libs/knockout/3.4.2/knockout-min',
        'bootstrap': '//cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min',
        'ko-prerendered' : '//cdnjs.cloudflare.com/ajax/libs/knockout-pre-rendered/0.9.1-beta/knockout-pre-rendered.min',
        'ko-contenteditable' : 'app/plugins/knockout-contenteditable/dest/knockout-contenteditable',
        'icon-picker' : '//cdnjs.cloudflare.com/ajax/libs/bootstrap-iconpicker/1.9.0/js/bootstrap-iconpicker.min',
        'icons' : '//cdnjs.cloudflare.com/ajax/libs/bootstrap-iconpicker/1.9.0/js/bootstrap-iconpicker-iconset-all.min',
        'intercooler' : '//cdnjs.cloudflare.com/ajax/libs/intercooler-js/1.2.1/intercooler.min',
        'app': '../app'
    },
    shim: { 
    	'icon-picker': ['jquery', 'bootstrap', 'icons'],
    	'knockout' : ['jquery'],
        'intercooler' : ['jquery'],
        'bootstrap' : ['jquery'],
        'ko-prerendered' : ['knockout', 'jquery'],
        'ko-contenteditable' :  {
        	'deps': ['knockout', 'jquery']
        }
    }
};