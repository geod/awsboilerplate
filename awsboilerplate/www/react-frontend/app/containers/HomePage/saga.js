import {put, takeEvery, takeLatest} from 'redux-saga/effects';
import {SUBMIT_BACKGROUND_JOB, BACKGROUND_JOB_STATUS_POLL} from "./constants";
import {backgroundJobAccepted, backgroundJobRejected, backgroundJobStatusResult} from "./actions";

/**
 * Submit a background job
 */

 function extractRootDomain(url) {
    var domain = extractHostname(url),
        splitArr = domain.split('.'),
        arrLen = splitArr.length;

    //extracting the root domain here
    //if there is a subdomain
    if (arrLen > 2) {
        domain = splitArr[arrLen - 2] + '.' + splitArr[arrLen - 1];
        //check to see if it's using a Country Code Top Level Domain (ccTLD) (i.e. ".me.uk")
        if (splitArr[arrLen - 2].length == 2 && splitArr[arrLen - 1].length == 2) {
            //this is using a ccTLD
            domain = splitArr[arrLen - 3] + '.' + domain;
        }
    }
    return domain;
}

export function* submitBackgroundJob(action) {
  try {
    //https://api.awsboilerplate.io/prod/job
    // Call our request helper (see 'utils/request')
    url = `https://api.${extractRootDomain(window.location.hostname)}`
    const job_accept = yield fetch("${url}/prod/job", {method: "POST", body: JSON.stringify({'number': action.number})})
    const job_response = JSON.parse(job_accept._bodyText);
    yield put(backgroundJobAccepted(job_response["href"], job_response["id"]));
  } catch (err) {
    yield put(backgroundJobRejected(err));
  }
}

/**
 * Get the status of the background jobs (over simplification to have single endpoint vs status and result)
 */
export function* getBackgroundJobStatus(action) {
  try {
    // Call our request helper (see 'utils/request')
    const job_status_request = yield fetch("/api/job")
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
  // Watches for SUBMIT_BACKGROUND_TASK actions and calls getRepos when one comes in.
  // By using `takeLatest` only the result of the latest API call is applied.
  // It returns task descriptor (just like fork) so we can continue execution
  // It will be cancelled automatically on component unmount
  yield takeEvery(SUBMIT_BACKGROUND_JOB, submitBackgroundJob);
  yield takeLatest(BACKGROUND_JOB_STATUS_POLL, getBackgroundJobStatus);
}
