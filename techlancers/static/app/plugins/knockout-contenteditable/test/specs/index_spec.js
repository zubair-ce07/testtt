import '../../src/index';

describe('contenteditable', () => {
    const vm = {};
    const body = document.querySelector('body');

    beforeEach(() => {
        body.innerHTML = `
            <div id="test">
                <div data-bind="contenteditable: html" contenteditable="true"></div>
            </div>
        `;
    });

    afterEach(() => {
        body.innerHTML = '';
    });

    it('should register as two way binding', () => {
        expect(ko.expressionRewriting.twoWayBindings.contenteditable).toBe(true);

    });

    it('should update view if model changed.', () => {
        const test = 'test';
        const node = document.querySelector('[contenteditable]');

        vm.html = ko.observable('');
        ko.applyBindings(vm, document.querySelector('#test'));

        vm.html(test);

        expect(vm.html()).toBe(test);
        expect(node.innerHTML).toBe(test);
    });

    it('should update modal if view changed (keydown).', () => {
        const test = 'test';
        const event = 'keydown';
        const node = document.querySelector('[contenteditable]');

        vm.html = ko.observable('');
        ko.applyBindings(vm, document.querySelector('#test'));

        node.innerHTML = test;
        ko.utils.triggerEvent(node, event);

        expect(vm.html()).toBe(test);
        expect(node.innerHTML).toBe(test);
    });


    it('should update modal if view changed (keyup).', () => {
        const test = 'test';
        const event = 'keyup';
        const node = document.querySelector('[contenteditable]');

        vm.html = ko.observable('');
        ko.applyBindings(vm, document.querySelector('#test'));

        node.innerHTML = test;
        ko.utils.triggerEvent(node, event);

        expect(vm.html()).toBe(test);
        expect(node.innerHTML).toBe(test);
    });

    it('should update modal if view changed (blur).', () => {
        const test = 'test';
        const event = 'blur';
        const node = document.querySelector('[contenteditable]');

        vm.html = ko.observable('');
        ko.applyBindings(vm, document.querySelector('#test'));

        node.innerHTML = test;
        ko.utils.triggerEvent(node, event);

        expect(vm.html()).toBe(test);
        expect(node.innerHTML).toBe(test);
    });

    it('should call decode before update view', () => {
        const test = 'test';

        vm.html = { value: ko.observable(''), decode() {} };
        spyOn(vm.html, 'decode');
        ko.applyBindings(vm, document.querySelector('#test'));

        vm.html.value(test);

        expect(vm.html.decode).toHaveBeenCalled();
        expect(vm.html.decode.calls.first().args[0]).toBe('');
        expect(vm.html.decode.calls.mostRecent().args[0]).toBe(test);
    });

    it('should call encode before update modal', () => {
        const test = 'test';
        const event = 'blur';
        const node = document.querySelector('[contenteditable]');

        vm.html = { value: ko.observable(''), encode() {} };
        spyOn(vm.html, 'encode');
        ko.applyBindings(vm, document.querySelector('#test'));

        node.innerHTML = test;
        ko.utils.triggerEvent(node, event);

        expect(vm.html.encode).toHaveBeenCalled();
        expect(vm.html.encode.calls.first().args[0]).toBe(test);
        expect(vm.html.encode.calls.first().args[1]).toBe(event);
    });

    it('should use decode before update view', () => {
        const html = '<br>';
        const entity = '&lt;br&gt;';
        const node = document.querySelector('[contenteditable]');

        vm.html = {
            value: ko.observable(entity),
            encode(elementValue) {
                return elementValue.replace(html, entity);
            },
            decode(elementValue) {
                return elementValue.replace(entity, html);
            }
        };
        ko.applyBindings(vm, document.querySelector('#test'));

        expect(vm.html.value()).toBe(entity);
        expect(node.innerHTML).toBe(html);
    });

    it('should use encode before update model', () => {
        const html = '<br>';
        const entity = '&lt;br&gt;';
        const event = 'blur';
        const node = document.querySelector('[contenteditable]');

        vm.html = {
            value: ko.observable(''),
            encode(elementValue) {
                return elementValue.replace(html, entity);
            },
            decode(elementValue) {
                return elementValue.replace(entity, html);
            }
        };
        ko.applyBindings(vm, document.querySelector('#test'));

        node.innerHTML = html;
        ko.utils.triggerEvent(node, event);

        expect(vm.html.value()).toBe(entity);
        expect(node.innerHTML).toBe(html);
    });
});
