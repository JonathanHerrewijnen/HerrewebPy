import logo from '../static/logo.svg';
import '../static/App.css';
import Projects from './Projects';
import AppHeader from './AppHeader';

function App() {
  return (
    <div className="App">
      <AppHeader />
      <Projects />
    </div>
  );
}

export default App;
