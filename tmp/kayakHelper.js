"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
class kayakHelper {
    getPrice(element) {
        return element.match(/\$((?:\d|\,)*\.?\d+)/g) != null ? parseFloat(element.match(/\$((?:\d|\,)*\.?\d+)/g)[0].split("$")[1]) : null;
    }
}
exports.kayakHelper = kayakHelper;
//# sourceMappingURL=data:application/json;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoia2F5YWtIZWxwZXIuanMiLCJzb3VyY2VSb290IjoiIiwic291cmNlcyI6WyIuLi9rYXlha0hlbHBlci50cyJdLCJuYW1lcyI6W10sIm1hcHBpbmdzIjoiOztBQUNBO0lBRUksUUFBUSxDQUFDLE9BQWU7UUFDcEIsT0FBTyxPQUFPLENBQUMsS0FBSyxDQUFDLHVCQUF1QixDQUFDLElBQUksSUFBSSxDQUFDLENBQUMsQ0FBQyxVQUFVLENBQUMsT0FBTyxDQUFDLEtBQUssQ0FBQyx1QkFBdUIsQ0FBQyxDQUFDLENBQUMsQ0FBQyxDQUFDLEtBQUssQ0FBQyxHQUFHLENBQUMsQ0FBQyxDQUFDLENBQUMsQ0FBQyxDQUFDLENBQUMsQ0FBQyxJQUFJLENBQUM7SUFDdkksQ0FBQztDQUNKO0FBTEQsa0NBS0MifQ==