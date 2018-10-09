import { put, call, takeEvery } from 'redux-saga/effects'
import * as api from "../apiCaller";


function* fetchMonthlyData(action) {
    try {

        const data = yield call(api.get, 'weather/average-monthly/'+action.payload);
        debugger;

        yield put({type: "FETCH_MONTHLY_WEATHER_SUCCEEDED", payload: data})
    } catch (error) {
        yield put({type: "FETCH_MONTHLY_WEATHER_FAILED", error})
    }
}

function* fetchYearlyData(action) {
    try {
        const data = yield call(api.get, 'weather/yearly/'+action.payload);
        debugger;
        yield put({type: "FETCH_YEARLY_WEATHER_SUCCEEDED", payload: data})
    } catch (error) {
        yield put({type: "FETCH_YEARLY_WEATHER_FAILED", error})
    }

}

function* resetWeather(action){
    yield put({type: 'RESET_MONTHLY_WEATHER'});
    yield put({type: 'RESET_YEARLY_WEATHER'});
}


export default function* watchWeather() {
    yield takeEvery('FETCH_MONTHLY_WEATHER', fetchMonthlyData);
    yield takeEvery('FETCH_YEARLY_WEATHER', fetchYearlyData);
    yield takeEvery('RESET_WEATHER', resetWeather)

}