import {put, call, takeEvery} from 'redux-saga/effects'
import * as api from '../apiCaller'

function* fetchCitiesData(action) {
    try {

        const data = yield call(api.get, 'weather/cities/');
        yield put({type: "FETCH_CITIES_SUCCEEDED", payload: data})

    } catch (error) {
        yield put({type: "FETCH_CITIES_FAILED", error})
    }
}

export default function* watchCities() {
    yield takeEvery('FETCH_CITIES', fetchCitiesData);
}