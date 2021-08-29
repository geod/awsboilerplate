/**
 * Homepage selectors
 */

import { createSelector } from 'reselect';
import { initialState } from './reducer';

const selectHome = state => state.home || initialState;

const makeSelectHello = () => createSelector(selectHome, homeState => homeState.hello_to);
const makeSelectJobs = () => createSelector(selectHome, homeState => homeState.accepted_jobs);
const makeSelectJobResults = () => createSelector(selectHome, homeState => homeState.finished_jobs);


export { makeSelectHello, makeSelectJobs, makeSelectJobResults };

