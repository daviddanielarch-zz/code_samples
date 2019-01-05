import React from 'react';
import { TableRow } from './TableRow';

export const ResultsTable = data => (
  <div>
    <table>
      <thead>
      <tr>
        <th> Overall Place </th>
        <th> Bib </th>
        <th> Name </th>
        <th> Time </th>
        <th> State </th>
        <th> Country </th>
        <th> Division </th>
        <th> Gender </th>
        <th></th>
      </tr>
      </thead>
      <tbody>
        {data.map(elem => TableRow(elem))}
      </tbody>
    </table>
  </div>
);
