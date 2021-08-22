/*
 * HomePage Messages
 *
 * This contains all the text for the HomePage component.
 */
import { defineMessages } from 'react-intl';

export const scope = 'boilerplate.containers.HomePage';

export default defineMessages({
  startProjectHeader: {
    id: `${scope}.start_project.header`,
    defaultMessage: 'awsboilerplate.io Live Demo',
  },
  startProjectMessage: {
    id: `${scope}.start_project.message`,
    defaultMessage:
      'This site is built and deployed by the awsboilerplate project',
  }
});
