/**
 * Homepage selectors
 */

import { createSelector } from 'reselect';
import { initialState } from './reducer';

const selectHome = state => state.home || initialState;
const makeSelectJobs = () => createSelector(selectHome, homeState => homeState.jobs);


const makeSelectJobResults = () => createSelector(selectHome, homeState => homeState.jobs_result);

export { makeSelectJobs, makeSelectJobResults };

