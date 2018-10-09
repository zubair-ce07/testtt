import {put, call, takeEvery} from 'redux-saga/effects'
import * as api from '../apiCaller'

function* fetchYearsData(action) {
    try {
        const data = yield call(api.get, 'weather/years/'+action.payload);

        if(data)
            yield put({type: "FETCH_YEAR_SUCCEEDED", payload: data});
        else
            yield put({type: "FETCH_YEAR_EMPTY", payload: data});

    } catch (error) {
        yield put({type: "FETCH_YEARS_FAILED", error})
    }
}

export default function* watchYears() {
    yield takeEvery('FETCH_YEARS', fetchYearsData);
}
