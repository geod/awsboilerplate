import React from 'react';
import { FormattedMessage } from 'react-intl';

import A from './A';
import Img from './Img';
import NavBar from './NavBar';
import HeaderLink from './HeaderLink';
import Banner from './banner.jpg';
import messages from './messages';

function Header() {
  return (
    <div>
      <A href="https://github.com/geod/awsboilerplate/">
        <Img src={Banner} alt="awsboilerplate - Logo" />
      </A>
      <NavBar>
        <HeaderLink to="/">
          <FormattedMessage {...messages.home} />
        </HeaderLink>
      </NavBar>
    </div>
  );
}

export default Header;
