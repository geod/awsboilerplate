import React, { useEffect, memo } from 'react';
import PropTypes from 'prop-types';
import { Helmet } from 'react-helmet';
import { FormattedMessage } from 'react-intl';
import { connect } from 'react-redux';
import { compose } from 'redux';

import Hero from './Hero';
import Features from './Features';
import Motivation from './Motivation';
import LambdaDemo from '../LambdaDemo';
import messages from './messages';

import H2 from 'components/H2';
import Header from 'components/Header';

import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.min.css';

const key = 'home';

export function HomePage({}) {

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
        <Hero />
        <Motivation />
        <Features />
        <LambdaDemo/>
      </div>
    </article>
  );
}



export default compose()(HomePage);
