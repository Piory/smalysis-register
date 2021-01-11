import React from 'react';

import { Button } from '@material-ui/core';

const App: React.FC = (): JSX.Element => {
  return (
    <Button variant='contained' color='primary' onClick={() => window.api.analyzeResult()}>
      OCR
    </Button>
  );
};

export default App;
