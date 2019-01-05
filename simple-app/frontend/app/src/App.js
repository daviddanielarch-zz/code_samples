import React, { Component } from 'react';
import { MarathonSelector } from './containers/MarathonSelector.jsx';
import { MarathonResults } from './containers/MarathonResults';

class App extends Component {
  constructor(props) {
    super(props);
    this.selectMarathon = this.selectMarathon.bind(this);
    this.doneFetchingMarathons = this.doneFetchingMarathons.bind(this);
    this.state = {
      selectedMarathon: null, marathonName: null, marathonDate: null, isFetchingMarathons: true,
    };
  }

  doneFetchingMarathons() {
    this.setState({ isFetchingMarathons: false });
  }

  selectMarathon(marathonId, marathonName, marathonDate) {
    this.setState({ selectedMarathon: marathonId, marathonName, marathonDate });
  }

  render() {
    const {
      isFetchingMarathons, selectedMarathon, marathonDate, marathonName,
    } = this.state;
    return (
      <div>
        <div>
          {marathonName}
        </div>
        <div>
          {marathonDate}
        </div>
        <MarathonSelector selectMarathon={this.selectMarathon} doneFetchingMarathons={this.doneFetchingMarathons} />
        {!isFetchingMarathons && <MarathonResults marathonId={selectedMarathon} />}
      </div>
    );
  }
}

export default App;
