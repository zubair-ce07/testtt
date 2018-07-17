(function ($) {

    $.fn.validate = function (options) {
        const settings = $.extend({
                pattern: null,
                empty: null,
                invalid: null,
                valid: null
            },
            options
        );
        const valueLength = $(this).val().trim().length;
        if (valueLength === 0 && $.isFunction(settings.empty)){
            settings.empty.call(this);
        }else if (settings.pattern !== null && !settings.pattern.test($(this).val())){
            if ($.isFunction(settings.invalid)){
                settings.invalid.call(this);
            }
        }else {
            if ($.isFunction(settings.valid)) {
                settings.valid.call(this);
            }
        }
        return this;
    };//validate

    $.fn.equalTo = function (options) {
        const settings = $.extend({
                id: null,
                equal: null,
                notEqual: null
            },
            options
        );
        if (settings.id !== null){
            if ($(this).val() === $(settings.id).val() && $.isFunction(settings.equal)){
                settings.equal.call(this);
            }else{
                if ($.isFunction(settings.notEqual))
                    settings.notEqual.call(this);
            }
        }
        return this;
    };//equalTo

    $.fn.isExist = function (options) {
        const settings = $.extend({
                url: null,
                exist: null,
                notExist: null
            },
            options
        );
        if (settings.url !== null){
            $.ajax({
                type: "GET",
                url: settings.url+$(this).val(),
                dataType: 'json',
                success: function (response) {
                    if (response.status === true && $.isFunction(settings.exist)) {
                        settings.exist.call(this);
                    }else{
                        if ($.isFunction(settings.notExist))
                            settings.notExist.call(this);
                    }
                }//success
            });//ajax_request
        }
    };//isExist

}(jQuery));