function loadData(){

    var $body = $('body');
    var $wikiElem = $('#wikipedia-links');
    var $nytHeaderElem = $('#nytimes-header');
    var $nytElem = $('#nytimes-articles');
    var $greeting = $('#greeting');

    // clear out old data before new request
    $wikiElem.text("");
    $nytElem.text("");

    // load streetview
    var street = $('#street').val();
    var city = $('#city').val();
    var address = street + ',' + city;
    $greeting.text('So you want to live at ' + address + '?' );
    var streetviewURL = "http://maps.googleapis.com/maps/api/streetview?size=600x400&location="+address+'';
    $body.append('<img class="bgimg" src="'+streetviewURL+'">');

    //load ny-articles
    var nytimesURL = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?q='+ city + "&sort=newest&api-key=bd9368d906ea4fab944590d0dc7310ab";
    $.getJSON(nytimesURL, function(data){

        $nytHeaderElem.text('New York Times Articles About ' + city);
        articles = data.response.docs;

        for(var item = 0; item<articles.length; item++){
            article = articles[item];
            $nytElem.append('<li class="article">'+
                '<a href="'+ article.web_url+'">'+ article.headline.main+'</a>'+
                '<p>'+ article.snippet+'</p>'+
                '<\li>');
        };
    }).error(function(e) {
        $nytHeaderElem.text('New York Times Articles Could Not Be Loaded');
    });

    //load wikepedia links

    var wikiTimeOut = setTimeout(function(){
        $wikiElem.text('failed to get wikipedia resources');
    }, 8000);
    var wikipediaURL = 'https://en.wikipedia.org/w/api.php?action=opensearch&search='+
        city+'&format=json&callback=wikiCallback';
    $.ajax({
        url: wikipediaURL,
        dataType: "jsonp",
        success: function(response){

        var links = response[1];

        for (var item = 0; item < links.length; item++) {
            link = links[item];
            var url = 'https://en.wikipedia.org/wiki/'+link;
            $wikiElem.append('<li><a href="' + url + '">' + link + '</a><\li>');
        };

        clearTimeout(wikiTimeOut);
    }
    });


    return false;
};

$('#form-container').submit(loadData);
