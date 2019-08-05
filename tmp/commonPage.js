"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : new P(function (resolve) { resolve(result.value); }).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", { value: true });
const protractor_1 = require("protractor");
class commonPage {
    waitUntillElementAppears(element) {
        return __awaiter(this, void 0, void 0, function* () {
            let until = yield protractor_1.protractor.ExpectedConditions;
            protractor_1.browser.wait(until.visibilityOf(element), 30000, 'element taking too long to appear in the DOM');
        });
    }
    patternToBePresentInElement(elementFinder, pattern) {
        let EC = protractor_1.protractor.ExpectedConditions;
        let matchesPattern = function () {
            return elementFinder.getText().then(function (actualText) {
                return actualText.search(pattern) !== -1;
            });
        };
        return EC.and(EC.presenceOf(elementFinder), matchesPattern);
    }
    ;
}
exports.commonPage = commonPage;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiY29tbW9uUGFnZS5qcyIsInNvdXJjZVJvb3QiOiIiLCJzb3VyY2VzIjpbIi4uL2NvbW1vblBhZ2UudHMiXSwibmFtZXMiOltdLCJtYXBwaW5ncyI6Ijs7Ozs7Ozs7OztBQUFBLDJDQUF5STtBQUV6STtJQUVVLHdCQUF3QixDQUFDLE9BQVk7O1lBQ3ZDLElBQUksS0FBSyxHQUFpQyxNQUFNLHVCQUFVLENBQUMsa0JBQWtCLENBQUM7WUFDOUUsb0JBQU8sQ0FBQyxJQUFJLENBQ1osS0FBSyxDQUFDLFlBQVksQ0FBQyxPQUFPLENBQUMsRUFDM0IsS0FBSyxFQUFFLDhDQUE4QyxDQUFDLENBQUM7UUFDM0QsQ0FBQztLQUFBO0lBRUQsMkJBQTJCLENBQUMsYUFBNEIsRUFBRSxPQUFlO1FBQ3JFLElBQUksRUFBRSxHQUFHLHVCQUFVLENBQUMsa0JBQWtCLENBQUM7UUFDdkMsSUFBSSxjQUFjLEdBQUc7WUFDakIsT0FBTyxhQUFhLENBQUMsT0FBTyxFQUFFLENBQUMsSUFBSSxDQUFDLFVBQVMsVUFBa0I7Z0JBQy9ELE9BQU8sVUFBVSxDQUFDLE1BQU0sQ0FBQyxPQUFPLENBQUMsS0FBSyxDQUFDLENBQUMsQ0FBQztZQUN6QyxDQUFDLENBQUMsQ0FBQztRQUNQLENBQUMsQ0FBQztRQUNGLE9BQU8sRUFBRSxDQUFDLEdBQUcsQ0FBQyxFQUFFLENBQUMsVUFBVSxDQUFDLGFBQWEsQ0FBQyxFQUFFLGNBQWMsQ0FBQyxDQUFDO0lBQ2hFLENBQUM7SUFBQSxDQUFDO0NBRUw7QUFuQkQsZ0NBbUJDIn0=