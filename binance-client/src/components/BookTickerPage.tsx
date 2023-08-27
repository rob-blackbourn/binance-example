import React, { useEffect, useState } from 'react'

import Table from '@mui/material/Table'
import TableBody from '@mui/material/TableBody'
import TableCell from '@mui/material/TableCell'
import TableContainer from '@mui/material/TableContainer'
import TableHead from '@mui/material/TableHead'
import TableRow from '@mui/material/TableRow'

import { queryGraphQL } from '../api'

export interface BookTicker {
  updateId: string
  symbol: string
  bidPrice: number
  bidQuantity: number
  askPrice: number
  askQuantity: number
}

export interface BookTickerPageProps {
  symbols: string[]
}

export const BookTickerPage: React.FC<BookTickerPageProps> = ({ symbols }) => {
  const [bookTickers, setBookTickers] = useState<Record<string, BookTicker>>({})

  useEffect(() => {
    const subscription = queryGraphQL(
      `subscription BookTickers($symbols: [String!]!) {
        bookTickers(symbols: $symbols)  {
            updateId
            symbol
            bidPrice
            bidQuantity
            askPrice
            askQuantity
        }
        }
      `,
      {
        symbols
      },
      error => console.error(error),
      response => {
        const bookTicker = response.data.bookTickers as BookTicker
        setBookTickers(prev => ({ ...prev, [bookTicker.symbol]: bookTicker }))
      }
    )

    return () => subscription.unsubscribe()
  }, [setBookTickers, symbols])

  // return <div>Hello</div>
  const data = Object.values(bookTickers) as BookTicker[]
  console.log(data)

  return (
    <TableContainer>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell component="th">Ccy</TableCell>
            <TableCell align="right">Bid</TableCell>
            <TableCell align="right">Qty</TableCell>
            <TableCell align="right">Ask</TableCell>
            <TableCell align="right">Qty</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {data.map(bookTicker => (
            <TableRow>
              <TableCell component="th">{bookTicker.symbol}</TableCell>
              <TableCell align="right">{bookTicker.bidPrice}</TableCell>
              <TableCell align="right">{bookTicker.bidQuantity}</TableCell>
              <TableCell align="right">{bookTicker.askPrice}</TableCell>
              <TableCell align="right">{bookTicker.askQuantity}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  )
}
