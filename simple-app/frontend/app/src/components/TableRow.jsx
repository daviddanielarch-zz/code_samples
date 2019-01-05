import React from 'react';

export const TableRow = data => (
  <tr key={data.bib}>
    <td>{data.place}</td>
    <td>{data.bib}</td>
    <td>{`${data.firstName} ${data.lastName}`}</td>
    <td>{data.time}</td>
    <td>{data.city}</td>
    <td>{data.country}</td>
    <td>{data.division}</td>
    <td>{data.gender}</td>
    <td>View</td>
  </tr>
);
