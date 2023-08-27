import CssBaseline from '@mui/material/CssBaseline'

import { BookTickerPage } from './components/BookTickerPage'

export default function App() {
  return (
    <div>
      <CssBaseline />
      <BookTickerPage symbols={['bnbusdt', 'btcusdt', 'ethusdt']} />
    </div>
  )
}
