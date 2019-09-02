'use strict';

require.main.require = (testOption) =>{
	if (testOption == './src/database') {
		return {
			client: {
				db: {},
				collection: function () {return this},
				count: function (query) {return this.db[query.key] ? 1 : 0;},
				insert: function (obj) {this.db = obj; return "key inserted!"},
				findOne: function (query) {return this.db.value},
				update: function (key, obj) {
					
					if (obj.$unset != undefined) {
						let deleteId = (Object.keys(obj.$unset)[0].split('.')[1])
						if (this.db.value[deleteId]) {
							delete this.db.value[deleteId];
							return { result: { "nModified" : 1 }}
						} else {
							return { result: { "nModified" : 0 }}
						}
					} else {
						let badgeId = Object.keys(obj.$set)[0].split('.')[1]
						this.db.value[badgeId] = obj.$set[`value.${badgeId}`]
					}
				},
			},
		}
	} else if (testOption == "./src/controllers") {
		return {}
	} else {
		throw Error("Unknown `require.main.require` option encountered!")
	}
}
