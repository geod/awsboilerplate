/*
 * HomeReducer
 *
 * The reducer takes care of our data. Using actions, we can
 * update our application state. To add a new action,
 * add it to the switch statement in the reducer function
 *
 */

import produce from 'immer';
import {
  BACKGROUND_JOB_LAUNCH_FAIL,
  BACKGROUND_JOB_ACCEPTED,
  SUBMIT_BACKGROUND_JOB,
  BACKGROUND_JOB_RESULT, BACKGROUND_JOB_STATUS_POLL
} from './constants';

// The initial state of the App
export const initialState = {
  accepted_jobs: [],
  finished_jobs: []
};

/* eslint-disable default-case, no-param-reassign */
const homeReducer = (state = initialState, action) =>
  produce(state, draft => {
    switch (action.type) {
      case SUBMIT_BACKGROUND_JOB:
        break;
      case BACKGROUND_JOB_ACCEPTED:
        draft.accepted_jobs.push({"id": action.id, "href": action.href});
        break;
      case BACKGROUND_JOB_RESULT:
        debugger;
        draft.finished_jobs = [];
        draft.finished_jobs.push(action.jobs_result[0]);
        break;
    }
  });

export default homeReducer;
