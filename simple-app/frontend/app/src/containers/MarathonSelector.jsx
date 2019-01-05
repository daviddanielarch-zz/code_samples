import React, { Component } from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';


export class MarathonSelector extends Component {
  constructor(props) {
    super(props);
    this.setNewMarathon = this.setNewMarathon.bind(this);
    this.state = { marathons: [] };
  }

  setNewMarathon(e) {
    const { marathons } = this.state;
    const marathonInfo = marathons.find(m => m.id === Number(e.target.value));
    this.props.selectMarathon(Number(e.target.value), marathonInfo.name, marathonInfo.date);
  }

  componentDidMount() {
    axios.get('api/marathon/list')
      .then(response => response.data)
      .then((data) => {
        const firstMarathon = data.data[0];
        this.props.selectMarathon(firstMarathon.id, firstMarathon.name, firstMarathon.date);
        this.setState({ marathons: data.data });
        this.props.doneFetchingMarathons();
      })
      .catch(error => console.log(error));
  }

  render() {
    const { marathons } = this.state;
    return (
      <div style={{ textAlign: 'right' }}>
        <select onChange={this.setNewMarathon}>
          {marathons.map(marathon => (
            <option key={marathon.id} value={marathon.id}>
              {marathon.name}
            </option>
          ))}
        </select>
      </div>
    );
  }
}

MarathonSelector.propTypes = {
  selectMarathon: PropTypes.func.isRequired,
  doneFetchingMarathons: PropTypes.func.isRequired,
};
