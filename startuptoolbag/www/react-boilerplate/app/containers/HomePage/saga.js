/**
 * Gets the repositories of the user from Github
 */

import { call, put, select, takeEvery } from 'redux-saga/effects';
import { reposLoaded, repoLoadingError } from 'containers/App/actions';

import request from 'utils/request';
import { makeSelectUsername } from 'containers/HomePage/selectors';
import {SUBMIT_BACKGROUND_JOB} from "./constants";
import {backgroundJobAccepted, backgroundJobRejected} from "./actions";

/**
 * Github repos request/response handler
 */
export function* launchTask(action) {
  try {
    // Call our request helper (see 'utils/request')
    const job_accept = yield fetch("/api/job", {method: "POST", body: JSON.stringify({'number': action.number})})
    const job_response = JSON.parse(job_accept._bodyText);
    yield put(backgroundJobAccepted(job_response["href"], job_response["id"]));
  } catch (err) {
    yield put(backgroundJobRejected(err));
  }
}

/**
 * Root saga manages watcher lifecycle
 */
export default function* launchBackgroundTask() {
  // Watches for SUBMIT_BACKGROUND_TASK actions and calls getRepos when one comes in.
  // By using `takeLatest` only the result of the latest API call is applied.
  // It returns task descriptor (just like fork) so we can continue execution
  // It will be cancelled automatically on component unmount
  yield takeEvery(SUBMIT_BACKGROUND_JOB, launchTask);
}
