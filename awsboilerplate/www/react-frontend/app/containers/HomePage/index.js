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

import { makeSelectHello } from './selectors'
import { sayHelloRequest } from "./actions";
import { useInjectReducer } from 'utils/injectReducer';
import { useInjectSaga } from 'utils/injectSaga';
import H2 from 'components/H2';
import reducer from './reducer';
import saga from './saga';

const key = 'home';

export function HomePage({
  onSayHello,
  hello_to,
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
          <Form onSubmit={onSayHello}>
            <Input
                id="say"
                type="text"
              />
          </Form>
          Response From Lambda:{hello_to}
        </Section>
      </div>
    </article>
  );
}

HomePage.propTypes = {
  onSayHello: PropTypes.func,
  hello_to: PropTypes.string,
};

// Maps the redux store state to component properties
const mapStateToProps = createStructuredSelector({
  hello_to: makeSelectHello(),
});

// Maps dispatch actions onto the properties of the component. Return values are callable functions in the component
export function mapDispatchToProps(dispatch) {
  return {
    onSayHello: evt => {
      if (evt !== undefined && evt.preventDefault) evt.preventDefault();
        dispatch(sayHelloRequest(document.getElementById('say').value))
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
