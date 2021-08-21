import {call, put, takeEvery, takeLatest} from 'redux-saga/effects';
import {BACKGROUND_JOB_SUBMIT, BACKGROUND_JOB_STATUS_POLL, SAY_HELLO_REQUEST} from "./constants";
import {sayHelloResult, backgroundJobAccepted, backgroundJobRejected, backgroundJobStatusResult} from "./actions";
import axios from 'axios';

/**
 * Submit a background job
 */

const rootDomain = s => {
    const r =  /.*\.([^.]*[^0-9][^.]*\.[^.]*[^.0-9][^.]*$)/;
    return s.replace(r, '$1');
};

/**
 * Get the status of the background jobs (over simplification to have single endpoint vs status and result)
 */
export function* sayHello(action) {
  try {
    debugger;
    const root_domain = rootDomain(window.location.hostname);
    const full_path = "https://api." + root_domain + "/prod/hello?to=" + action.text;
    const { data } = yield axios.get(full_path)
    yield put(sayHelloResult(data.message, true));
  } catch (err) {
    yield put(sayHelloResult(err, false));
  }
}

export function* submitBackgroundJob(action) {
  try {
    const root_domain = rootDomain(window.location.hostname);
    const full_path = "https://api." + root_domain + "/prod/job"
    const job_accept = yield fetch(full_path, {method: "POST", body: JSON.stringify({'number': action.number})})
    const job_response = JSON.parse(job_accept._bodyText);
    yield put(backgroundJobAccepted(job_response["id"], job_response["href"], action.number));
  } catch (err) {
    yield put(backgroundJobRejected(err));
  }
}

/**
 * Get the status of the background jobs (over simplification to have single endpoint vs status and result)
 */
export function* getBackgroundJobStatus(action) {
  try {
    const root_domain = rootDomain(window.location.hostname);
    const full_path = "https://api." + root_domain + "/prod/job"
    const job_status_request = yield fetch(full_path)
    const job_status = JSON.parse(job_status_request._bodyText);
    yield put(backgroundJobStatusResult(job_status));
  } catch (err) {
    yield put(backgroundJobRejected(err));
  }
}


/**
 * Root saga manages watcher lifecycle
 */
export default function* launchBackgroundTask() {
  yield takeEvery(SAY_HELLO_REQUEST, sayHello);
  yield takeEvery(BACKGROUND_JOB_SUBMIT, submitBackgroundJob);
  yield takeLatest(BACKGROUND_JOB_STATUS_POLL, getBackgroundJobStatus);
}
