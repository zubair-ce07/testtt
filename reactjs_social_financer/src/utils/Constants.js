
class Constants {
  constructor() {
    this.baseUrl = 'http://127.0.0.1:8000/';
    this.url = 'http://127.0.0.1:8000/api/';
    this.loginPOST = this.url + 'accounts/login/';
    this.signupPOST = this.url + 'accounts/signup/';
    this.unpairedConsumersGET = this.url + 'accounts/consumers_list/';
    this.pairUserPOST = this.url + 'accounts/consumers_list/';
    this.pairedConsumerGET = this.url + 'accounts/my_consumers/';
    this.myDonorGET = this.url + 'accounts/my_donor/';
    this.myProfileGET = this.url + 'accounts/profile/';
    this.categoriesGET = this.url + 'category/get_categories/';
    this.feedbackPOST = this.url + 'feedback/post_feedback/';
    this.feedbackGET = this.url + 'feedback/get_feedback/'
    this.reportPOST = this.url + 'report/report/';
    this.mapUrl = 'https://www.google.com/maps/search/?api=1&query='
  }
}

var Singleton = (function () {
    var instance;

    function createInstance() {
        var object = new Constants();
        return object;
    }

    return {
        getInstance: function () {
            if (!instance) {
                instance = createInstance();
            }
            return instance;
        }
    };
})();

export default Singleton.getInstance();
