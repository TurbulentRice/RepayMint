import { render } from 'preact'
import { App } from './app.jsx'
import '../node_modules/bootstrap/dist/css/bootstrap.min.css';
import './index.css'

render(<App />, document.getElementById('app'))
