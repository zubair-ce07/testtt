exports.config = {
    framework: 'jasmine',
    seleniumAddress: 'http://localhost:4444/wd/hub',
    specs: ['spec.ts'],
    onPrepare() {
        require('ts-node').register({
            project: require('path').join(__dirname, './tsconfig.json') // Relative path of tsconfig.json file
        });
    }
};