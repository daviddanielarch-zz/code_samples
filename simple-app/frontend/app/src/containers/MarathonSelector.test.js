import React from 'react';
import { mount, shallow, configure } from 'enzyme';
import axios from 'axios';
import Adapter from 'enzyme-adapter-react-16';
import { MarathonSelector } from './MarathonSelector';

configure({ adapter: new Adapter() });


describe('<MarathonSelector/>', () => {
  let mockSelectMarathon = null;
  let mockDoneFetching = null;
  let promise = null;

  beforeEach(() => {
    mockSelectMarathon = jest.fn();
    mockDoneFetching = jest.fn();
    promise = Promise.resolve({ data: { data: [{ id: 1, name: 'SARASA', date: 'date' }] } });
    spyOn(axios, 'get').and.returnValue(promise);
  });

  it('retrieves marathon lists when mounted', () => {
    const wrapper = shallow(<MarathonSelector selectMarathon={mockSelectMarathon} doneFetchingMarathons={mockDoneFetching} />);
    expect(axios.get).toHaveBeenCalledWith('api/marathon/list');

    promise.then(() => {})
      .then(() => {
        expect(mockDoneFetching).toHaveBeenCalled();
        expect(mockSelectMarathon).toHaveBeenCalledWith(1, 'SARASA', 'date');
        expect(wrapper.state('marathons')).toEqual([{ id: 1, name: 'SARASA', date: 'date' }]);
      });
  });

  it('shows the marathon list', () => {
    const wrapper = shallow(<MarathonSelector selectMarathon={mockSelectMarathon} doneFetchingMarathons={mockDoneFetching} />);

    wrapper.setState({
      marathons:
      [{ id: 1, name: 'SARASA', date: 'date' },
        { id: 2, name: 'SARASA 2', date: 'date2' }],
    });
    wrapper.update();
    expect(wrapper.find('option').length).toEqual(2);
  });

  it('changes the selected marathon on click', () => {
    const wrapper = shallow(<MarathonSelector selectMarathon={mockSelectMarathon} doneFetchingMarathons={mockDoneFetching} />);

    wrapper.setState({
      marathons:
      [{ id: 1, name: 'SARASA', date: 'date' },
        { id: 2, name: 'SARASA 2', date: 'date2' }],
    });
    wrapper.find('select').simulate('change', { target: { value: 2 } });
    expect(mockSelectMarathon).toHaveBeenCalledWith(2, 'SARASA 2', 'date2');
  });
});
