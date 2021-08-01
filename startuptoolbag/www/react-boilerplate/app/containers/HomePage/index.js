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

import {makeSelectJobs} from './selectors'
import {submitBackgroundJob} from "./actions";
import { useInjectReducer } from 'utils/injectReducer';
import { useInjectSaga } from 'utils/injectSaga';
import H2 from 'components/H2';
import reducer from './reducer';
import saga from './saga';

const key = 'home';

export function HomePage({
  onSubmitBackgroundTask,
  jobs,
}) {
  useInjectReducer({ key, reducer });
  useInjectSaga({ key, saga });

//  useEffect(() => {
//    // When initial state username is not null, submit the form to load repos
//    if (username && username.trim().length > 0) onSubmitForm();
//  }, []);

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
          <Form onSubmit={onSubmitBackgroundTask}>
          Launch a background task (check if number is prime):
            <Input
                id="username"
                type="number"
              />
          </Form>
        </Section>
        <Section>
          {jobs.length}
        </Section>
      </div>
    </article>
  );
}

HomePage.propTypes = {
  onSubmitBackgroundTask: PropTypes.func,
  jobs: PropTypes.array,
};

// Maps the redux store state to component properties
const mapStateToProps = createStructuredSelector({
  jobs: makeSelectJobs(),
});

// Maps dispatch actions onto the properties of the component. Return values are callable functions in the component
export function mapDispatchToProps(dispatch) {
  return {
    onSubmitBackgroundTask: evt => {
      if (evt !== undefined && evt.preventDefault) evt.preventDefault();
      dispatch(submitBackgroundJob(evt.target.value))
    }
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
