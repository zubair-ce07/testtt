// Uses AMD or browser globals to create a module.

// If you want something that will also work in Node, see returnExports.js
// If you want to support other stricter CommonJS environments,
// or if you need to create a circular dependency, see commonJsStrict.js

// Defines a module "amdWeb" that depends on another module called "b".
// Note that the name of the module is implied by the file name. It is best
// if the file name and the exported global have matching names.

// If the 'b' module also uses this type of boilerplate, then
// in the browser, it will create a global .b that is used below.

// If you do not want to support the browser global path, then you
// can remove the `root` use and the passing of `this` as the first arg to
// the top function.

(function (root, factory) {
    if (typeof define === 'function' && define.amd) {
        // AMD. Register as an anonymous module.
        define(['knockout'], factory);
    } else {
        // Browser globals
        root.amdWeb = factory(root.b);
    }
}(typeof self !== 'undefined' ? self : this, function (ko) {
    ko.bindingHandlers['contenteditable'] = {
    init(element, valueAccessor, allBindings) {
        const value = valueAccessor();
        const config = ko.isObservable(value) ? { value: value } : value;
        const hasEncode = typeof config.encode === 'function';
        const hasDecode = typeof config.decode === 'function';
        const eventTypes = [ 'blur' ];

        function updateView() {
            const modelValue = ko.utils.unwrapObservable(config.value) || '';

            element.innerHTML = hasDecode ?
                config.decode(modelValue) : modelValue;
        }

        function updateModel(eventType, ev) {
            const elementValue = element.innerHTML;

            config.value(hasEncode ? config.encode(elementValue, eventType) : elementValue);
        }

        ko.utils.arrayForEach(eventTypes, (eventType) => {
            ko.utils.registerEventHandler(element, eventType, updateModel.bind(null, eventType));
        });
        ko.computed(updateView);
    }
    };
}));