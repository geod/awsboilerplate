/*
 * HomeConstants
 * Each action has a corresponding type, which the reducer knows and picks up on.
 * To avoid weird typos between the reducer and the actions, we save them as
 * constants here. We prefix them with 'yourproject/YourComponent' so we avoid
 * reducers accidentally picking up actions they shouldn't.
 *
 * Follow this format:
 * export const YOUR_ACTION_CONSTANT = 'yourproject/YourContainer/YOUR_ACTION_CONSTANT';
 */
export const BACKGROUND_JOB_SUBMIT = 'awsboilerplate/Home/BACKGROUND_JOB_SUBMIT';

export const BACKGROUND_JOB_ACCEPTED = 'awsboilerplate/Home/BACKGROUND_JOB_ACCEPTED';

export const BACKGROUND_JOB_LAUNCH_FAIL = 'awsboilerplate/Home/BACKGROUND_JOB_LAUNCH_FAIL';

export const BACKGROUND_JOB_RESULT = 'awsboilerplate/Home/BACKGROUND_JOB_RESULT';

export const BACKGROUND_JOB_STATUS_POLL = 'awsboilerplate/Home/BACKGROUND_JOB_STATUS_POLL';

export const SAY_HELLO_REQUEST = 'awsboilerplate/Home/SAY_HELLO_REQUEST';

export const SAY_HELLO_RESULT = 'awsboilerplate/Home/SAY_HELLO_RESULT';


