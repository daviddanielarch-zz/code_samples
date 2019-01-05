import React, { Component } from 'react';

export class Paginator extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    const links = [];
    for (let i = 1; i < this.props.totalPages; i++) {
      links.push(<a key={i} onClick={() => this.props.setPage(i)}>| {i} |</a>);
    }
    return (
      <div style={{ textAlign: 'center' }}>
        {links}
      </div>);
  }
}
