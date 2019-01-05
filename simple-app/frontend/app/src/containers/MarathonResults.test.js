import React from 'react';
import { mount, shallow, configure } from 'enzyme';
import axios from 'axios';
import Adapter from 'enzyme-adapter-react-16';
import { MarathonResults } from './MarathonResults';

configure({ adapter: new Adapter() });


describe('<MarathonResults/>', () => {
  it('retrieves marathon results when mounted', () => {
    const promise = Promise.resolve({ data: { data: [{ id: 1 }] } });
    spyOn(axios, 'get').and.returnValue(promise);

    const wrapper = shallow(<MarathonResults marathonId={1} />);
    expect(axios.get).toHaveBeenCalledWith('api/marathon/results', {
      params: {
        age_filter: null, hometown_filter: null, id: 1, page: 1,
      },
    });
  });
});
