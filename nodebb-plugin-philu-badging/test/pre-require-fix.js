'use strict';

require.main.require = () => ({
	client: {
		db: {},
		collection: function () {return this},
		count: function (key) {console.log(this.db[key]); return this.db[key] ? 1 : 0;},
		insert: function (obj) {this.db[obj.key] = obj.value; return "key inserted!"},
		findOne: function (key) {return this.db[key]}
	},
});
