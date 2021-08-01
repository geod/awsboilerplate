/*
 * HomePage
 *
 * This is the first thing users see of our App, at the '/' route
 */

import React, { useEffect, memo } from 'react';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';
import { FormattedMessage } from 'react-intl';
import { connect } from 'react-redux';
import { compose } from 'redux';
import { createStructuredSelector } from 'reselect';

import CenteredSection from './CenteredSection';
import Input from './Input';
import Form from './Form';
import Section from './Section';
import messages from './messages';

import {makeSelectJobs, makeSelectJobResults} from './selectors'
import {submitBackgroundJob} from "./actions";
import {pollCompletedJobs} from "./actions";
import { useInjectReducer } from 'utils/injectReducer';
import { useInjectSaga } from 'utils/injectSaga';
import H2 from 'components/H2';
import reducer from './reducer';
import saga from './saga';

const key = 'home';

export function HomePage({
  onSubmitBackgroundJob,
  onPollCompletedJobs,
  jobs,
  job_results
}) {
  useInjectReducer({ key, reducer });
  useInjectSaga({ key, saga });

  return (
    <article>
      <Helmet>
        <title>Home Page</title>
        <meta
          name="description"
          content="awsboilerplate.io"
        />
      </Helmet>
      <div>
        <CenteredSection>
          <H2>
            <FormattedMessage {...messages.startProjectHeader} />
          </H2>
          <p>
            <FormattedMessage {...messages.startProjectMessage} />
          </p>
        </CenteredSection>
        <Section>
          <Form onSubmit={onSubmitBackgroundJob}>
          Launch a background task (check if the number is prime):
            <Input
                id="numberprime"
                type="number"
              />
          </Form>
        </Section>
        <Section>
          Accepted Jobs
          {jobs.map(job => { return (<div key={job.id}>{job.href}</div>)})}
        </Section>
        <Section>
          Last 10 Jobs (Global)
          <button onClick={onPollCompletedJobs}>Refresh</button>
          {job_results.map(job_result => { return (<div key={job_result.id}>{JSON.stringify(job_result.id) }</div>)})}
        </Section>
      </div>
    </article>
  );
}

HomePage.propTypes = {
  onSubmitBackgroundJob: PropTypes.func,
  onPollCompletedJobs: PropTypes.func,
  jobs: PropTypes.array,
  job_results: PropTypes.array
};

// Maps the redux store state to component properties
const mapStateToProps = createStructuredSelector({
  jobs: makeSelectJobs(),
  job_results: makeSelectJobResults()
});

// Maps dispatch actions onto the properties of the component. Return values are callable functions in the component
export function mapDispatchToProps(dispatch) {
  return {
    onSubmitBackgroundJob: evt => {
      if (evt !== undefined && evt.preventDefault) evt.preventDefault();
      dispatch(submitBackgroundJob(evt.target.value))
    },
    onPollCompletedJobs: evt => dispatch(pollCompletedJobs())
  };
}

// https://react-redux.js.org/api/connect
const withConnect = connect(
  mapStateToProps,
  mapDispatchToProps,
);

export default compose(
  withConnect,
  memo,
)(HomePage);
