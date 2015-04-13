'use strict';

angular.module('powersuite.version', [
  'powersuite.version.interpolate-filter',
  'powersuite.version.version-directive'
])

.value('version', '0.1');
