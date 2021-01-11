import React from 'react';

import { Button } from '@material-ui/core';
import { useRecoilState } from 'recoil';
import countAtom from 'main/atoms/countAtoms';

const App: React.FC = (): JSX.Element => {
  const [count, setCount] = useRecoilState(countAtom);
  return (
    <div>
      <Button variant='contained' color='primary' onClick={() => setCount(count - 1)}>
        Down
      </Button>
      {count}
      <Button variant='contained' color='primary' onClick={() => setCount(count + 1)}>
        Up
      </Button>
    </div>
  );
};

export default App;
