import { BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import UploadePage from './UploadePage';
import Results from './Results';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<UploadePage />} />
        <Route path="/results" element={<Results />} />
      </Routes>
    </Router>
  );
}

export default App;
