knockout-contenteditable
=====

## Installation

```bash
npm install --save-dev knockout-contenteditable
```

## Usage

```html
<div data-bind="contenteditable: editable" contenteditable="true"></div>
```

```js
ko.applyBindings({
    editable: {
        value: ko.observable(),

        // @param {String} elementValue
        // @param {String} eventType trigger event type
        encode(elementValue, eventType) {
            return elementValue.replace('<br>', '&lt;br&gt;');
        },


        // @param {String} modelValue
        decode(modelValue) {
            return elementValue.replace('&lt;br&gt;', '<br>');
        }
    }
});
```

## License

MIT &copy; BinRui.Guan


