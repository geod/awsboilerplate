import React, { useEffect, memo } from 'react';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';
import { FormattedMessage } from 'react-intl';
import { connect } from 'react-redux';
import { compose } from 'redux';
import { createStructuredSelector } from 'reselect';

import Input from './Input';
import Form from './Form';
import messages from './messages';

import { makeSelectHello } from './selectors'
import { sayHelloRequest } from "./actions";
import { useInjectReducer } from 'utils/injectReducer';
import { useInjectSaga } from 'utils/injectSaga';
import H2 from 'components/H2';
import Header from 'components/Header';
import reducer from './reducer';
import saga from './saga';

import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.min.css';

const key = 'home';

export function LambdaDemo({
  onSayHello,
  hello_to,
}) {
  useInjectReducer({ key, reducer });
  useInjectSaga({ key, saga });

  return (
      <section className="bg-white py-5" >
      <div className="position-relative overflow-hidden p-3 p-md-5 m-md-3 text-center bg-light">
        <div className="text-center mb-5">
          <h1 className="fw-bolder">Live Demo</h1>
        </div>
        <div className="col-md-5 mx-auto">
          <p className="lead font-weight-normal">Back end <a href="https://github.com/geod/awsboilerplate/tree/master/awsboilerplate/app/lambda_hello_world">hello world lambda</a> already wired into the front end with redux, saga</p>
          <p className="lead font-weight-normal">Call it now ...</p>
        </div>
          <Form onSubmit={onSayHello}>
            My name is: <Input
                id="say"
                type="text"
              />
              <Button variant="primary" onClick={onSayHello}>Submit</Button>{' '}
          </Form>
          Response:{hello_to}
      </div>
      </section>
  );
}

LambdaDemo.propTypes = {
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
)(LambdaDemo);
