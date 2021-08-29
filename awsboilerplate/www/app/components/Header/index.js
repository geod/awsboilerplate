import React from 'react';
import { FormattedMessage } from 'react-intl';

import A from './A';
import NavBar from './NavBar';
import HeaderLink from './HeaderLink';
import Banner from './banner.jpg';
import messages from './messages';

import Image from 'react-bootstrap/Image';

function Header() {
  return (
    <div>
      <Image src={Banner} />
    </div>
  );
}

export default Header;


