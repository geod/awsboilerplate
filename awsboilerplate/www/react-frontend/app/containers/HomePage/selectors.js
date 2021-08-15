/**
 * Homepage selectors
 */

import { createSelector } from 'reselect';
import { initialState } from './reducer';

const selectHome = state => state.home || initialState;
const makeSelectJobs = () => createSelector(selectHome, homeState => homeState.accepted_jobs);
const makeSelectJobResults = () => createSelector(selectHome, homeState => homeState.finished_jobs);

export { makeSelectJobs, makeSelectJobResults };

