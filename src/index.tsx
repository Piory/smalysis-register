import { RecoilRoot } from 'recoil';
import { ThemeProvider, createMuiTheme } from '@material-ui/core/styles';
import App from 'main/component/App';
import React from 'react';
import ReactDOM from 'react-dom';
import reportWebVitals from 'main/reportWebVitals';

const theme = createMuiTheme({
  palette: {
    primary: {
      main: '#000',
    },
  },
});
ReactDOM.render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <RecoilRoot>
        <App />
      </RecoilRoot>
    </ThemeProvider>
  </React.StrictMode>,
  document.getElementById('root'),
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
