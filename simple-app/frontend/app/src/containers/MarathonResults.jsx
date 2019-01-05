import React, { Component } from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';
import { AgeSelector } from '../components/AgeSelector';
import { ResultsTable } from '../components/ResultsTable';
import { Paginator } from './Paginator';


export class MarathonResults extends Component {
  constructor(props) {
    super(props);
    this.setHomeTownFilter = this.setHomeTownFilter.bind(this);
    this.setAgeFilter = this.setAgeFilter.bind(this);
    this.setCurrentPage = this.setCurrentPage.bind(this);
    this.updateResults = this.updateResults.bind(this);
    this.state = {
      results: [], ageFilter: null, homeTownFilter: null, page: 1, hasNextPage: false, hasPrevPage: false, totalPages: 1,
    };
  }

  componentDidUpdate(prevProps) {
    if (this.props.marathonId !== prevProps.marathonId) {
      this.updateResults();
    }
  }

  componentDidMount() {
    this.updateResults();
  }

  setAgeFilter(e) {
    this.setState({ ageFilter: e.target.value }, this.updateResults);
  }

  setHomeTownFilter(e) {
    e.persist();
    this.setState({ homeTownFilter: e.target.value }, this.updateResults);
  }

  setCurrentPage(page) {
    this.setState({ page }, this.updateResults);
  }

  updateResults() {
    const { marathonId } = this.props;
    const { ageFilter, homeTownFilter, page } = this.state;

    axios.get('api/marathon/results', {
      params: {
        id: marathonId,
        age_filter: ageFilter,
        hometown_filter: homeTownFilter,
        page,
      },
    })
      .then(response => response.data)
      .then((data) => {
        this.setState({
          results: data.data,
          hasNextPage: data.has_next,
          hasPrevPage: data.has_previous,
          totalPages: data.total_pages,
        });
      });
  }

  render() {
    const {
      results, hasNextPage, hasPrevPage, totalPages,
    } = this.state;

    return (
      <div>
        <div style={{ textAlign: 'center' }}>
          <input type="text" name="search" />
          <button> Go </button>
          <input type="text" name="hometown" onChange={this.setHomeTownFilter} />
          <AgeSelector setAgeFilter={this.setAgeFilter} />
        </div>
        <div>
          {ResultsTable(results)}
          <Paginator setPage={this.setCurrentPage} hasNext={hasNextPage} hasPrev={hasPrevPage} totalPages={totalPages} />
        </div>
      </div>
    );
  }
}

MarathonResults.proptypes = {
  marathonId: PropTypes.number.isRequired,
};
