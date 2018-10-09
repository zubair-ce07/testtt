import {all} from 'redux-saga/effects'

import watchWeather from './weatherActions'
import watchCities from './cityActions'
import watchYears from './yearActions'

export default function* rootSaga() {
    yield all([
        watchWeather(),
        watchCities(),
        watchYears(),
    ])
}