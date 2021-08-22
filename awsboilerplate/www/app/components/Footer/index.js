import React from 'react';
import { FormattedMessage } from 'react-intl';

import A from 'components/A';
import LocaleToggle from 'containers/LocaleToggle';
import Wrapper from './Wrapper';
import messages from './messages';


function Footer() {
  return (
    <Wrapper>
      <section>
        <FormattedMessage {...messages.licenseMessage} />
      </section>
      <section>
        {/* <LocaleToggle /> */}
      </section>
      <section>
        <p>
        </p>
      </section>
    </Wrapper>
  );
}

export default Footer;
