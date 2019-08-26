'use strict';

require.main.require = (testOption) =>{
	if (testOption == './src/database') {
		return {
			client: {
				db: {},
				collection: function () {return this},
				count: function (key) {console.log(this.db[key]); return this.db[key] ? 1 : 0;},
				insert: function (obj) {this.db[obj.key] = obj.value; return "key inserted!"},
				findOne: function (key) {return this.db[key]}
			},
		}
	} else if (testOption == "./src/controllers") {
		return {}
	} else {
		throw Error("Unknown `require.main.require` option encountered!")
	}
}
