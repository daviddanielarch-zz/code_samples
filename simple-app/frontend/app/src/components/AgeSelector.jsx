import React from 'react';
import PropTypes from 'prop-types';

export const AgeSelector = props => (
  <select onClick={props.setAgeFilter}>
    <option value="" />
    <option value={1}>
      {'< 22'}
    </option>
    <option value={2}>
            22 - 40
    </option>
    <option value={3}>
            40 - 60
    </option>
    <option value={4}>
      {'> 60'}
    </option>
  </select>
);

AgeSelector.proptypes = {
  setAgeFilter: PropTypes.number.isRequired,
};
