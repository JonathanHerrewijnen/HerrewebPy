import logo from '../static/logo.svg';
import '../static/App.css';
import Projects from './Projects';
import AppHeader from './AppHeader';
import AppFooter from './AppFooter';

function App() {
  return (
    <div className="App">
      <AppHeader />
      <Projects />
      <AppFooter />
    </div>
  );
}

export default App;
