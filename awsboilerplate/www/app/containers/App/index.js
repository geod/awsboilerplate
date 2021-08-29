/**
 *
 * App
 *
 * This component is the skeleton around the actual pages, and should only
 * contain code that should be seen on all pages. (e.g. navigation bar)
 */
import React from 'react';
import { Helmet } from 'react-helmet';
import styled from 'styled-components';
import { Switch, Route } from 'react-router-dom';

import HomePage from 'containers/HomePage/Loadable';
import LambdaDemo from 'containers/LambdaDemo/Loadable';
import NotFoundPage from 'containers/NotFoundPage/Loadable';
import Header from 'components/Header';
import NavigationBar from 'components/NavigationBar';
import Footer from 'components/Footer';

import GlobalStyle from '../../global-styles';


export default function App() {
  return (
    <div>
      <Helmet
        titleTemplate="%s - AWS Boilerplate"
        defaultTitle="AWS Boilerplate"
      >
        <meta name="description" content="AWS Boilerplate React Web Front End" />
      </Helmet>

      <NavigationBar />
      <Switch>
        <Route exact path="/" component={HomePage} />
        <Route exact path="/LambdaDemo" component={LambdaDemo} />
        <Route path="" component={NotFoundPage} />
      </Switch>
      <Footer />
      <GlobalStyle />
    </div>
  );
}
