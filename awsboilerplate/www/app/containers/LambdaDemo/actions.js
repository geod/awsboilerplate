/*
 * Home Actions
 *
 * Actions change things in your application
 * Since this boilerplate uses a uni-directional data flow, specifically redux,
 * we have these actions which are the only way your application interacts with
 * your application state. This guarantees that your state is up to date and nobody
 * messes it up weirdly somewhere.
 *
 * To add a new Action:
 * 1) Import your constant
 * 2) Add a function like this:
 *    export function yourAction(var) {
 *        return { type: YOUR_ACTION_CONSTANT, var: var }
 *    }
 */

import {
  BACKGROUND_JOB_SUBMIT,
  BACKGROUND_JOB_ACCEPTED,
  BACKGROUND_JOB_LAUNCH_FAIL,
  BACKGROUND_JOB_STATUS_POLL,
  BACKGROUND_JOB_RESULT,
  SAY_HELLO_REQUEST,
  SAY_HELLO_RESULT
} from './constants';

export function sayHelloRequest(text) {
  return {
    type: SAY_HELLO_REQUEST,
    text,
  };
}

export function sayHelloResult(text, success) {
  return {
    type: SAY_HELLO_RESULT,
    text,
    success,
  };
}

/**
 * Changes the input field of the form
 *
 * @param  {string} username The new text of the input field
 *
 * @return {object} An action object with a type of CHANGE_USERNAME
 */
export function submitBackgroundJob(number) {
  return {
    type: BACKGROUND_JOB_SUBMIT,
    number,
  };
}

export function backgroundJobAccepted(id, href, number) {
  return {
    type: BACKGROUND_JOB_ACCEPTED,
    id: id,
    href: href,
    number: number
  };
}

export function backgroundJobRejected(status) {
  return {
    type: BACKGROUND_JOB_LAUNCH_FAIL,
  };
}


export function pollCompletedJobs(status) {
  return {
    type: BACKGROUND_JOB_STATUS_POLL
  };
}

export function backgroundJobStatusResult(jobs_result) {
  return {
    type: BACKGROUND_JOB_RESULT,
    jobs_result: jobs_result
  };
}


