# binance-client-howto

This document shows the steps used to create the basic binance client.

## Step 1 - Create the React project.

First we must create a react project. The most simple approach is to
use [`create-react-app`](https://create-react-app.dev/).

The flags specify that we are using `npm` as the package manager (rather than `yarn`)
and to use TypeScript rather than plain JavaScript.

The `create-react-app` application essentially clones a project. We need
to remove that git repository from that project and create a new one.

```bash
$ npx create-react-app binance-client --use-npm --template typescript
binance-client $ cd binance-client
binance-client $ rm -rf .git
binance-client $ git init
binance-client $ git add .
binance-client $ git commit -m 'Initial commit'
```

## Step 2 - Tidy up the default project.

The scaffold creates a project with a bunch of code we don't want.
This needs to be cleaned up.

No open the project in [VS code](https://code.visualstudio.com/).

To make the code formatting consistent we will use [prettier](https://prettier.io/).
Ensure the "prettier" VS code extension is installed, then add the following to the
`package.json`.

```json
  ...
  "prettier": {
    "tabWidth": 2,
    "semi": false,
    "singleQuote": true,
    "trailingComma": "none",
    "printWidth": 80,
    "arrowParens": "avoid",
    "bracketsSpacing": true,
    "bracketSameLine": false
  },
  ...
```

In order to enable automatic formatting create the file `.vscode/settings.json` with the following content:

```json
{
    "[typescript]": {
        "editor.formatOnSave": true
    },
    "[typescriptreact]": {
        "editor.formatOnSave": true
    }
}
```

Now we can start tidying. Change `src/App.tsx` to:

```ts
export default function App() {
  return (
    <div>
      Contents here
    </div>
  )
}
```

In `public/index.html` change `<title>React App</title>` to `<title>Binance Client</title>`.

Now remove the now unreferenced  `src/App.css`, `App.test.tsx`, and `logo.svg`.

Change the `README.md` to:

```md
# binance-client

An example binance client.
```

Add the changes to git.

```bash
$ git add .
$ git commit -m "Tidied up the react project"
```

## Step 3 - Setup material UI

This project will use a [material-ui](http://mui.com) library.

Open a terminal in VS code and add the following packages.

```bash
npm install @mui/material @emotion/react @emotion/styled @mui/icons-material
npm install @fontsource/roboto @fontsource/material-icons
```

Change the `src/index.css` to the following in order to support
material font icons without going to the internet:

```css
.material-icons {
  font-family: 'Material Icons';
  font-weight: normal;
  font-style: normal;
  font-size: 24px;  /* Preferred icon size */
  display: inline-block;
  line-height: 1;
  text-transform: none;
  letter-spacing: normal;
  word-wrap: normal;
  white-space: nowrap;
  direction: ltr;

  /* Support for all WebKit browsers. */
  -webkit-font-smoothing: antialiased;
  /* Support for Safari and Chrome. */
  text-rendering: optimizeLegibility;

  /* Support for Firefox. */
  -moz-osx-font-smoothing: grayscale;

  /* Support for IE. */
  font-feature-settings: 'liga';
}
```

Change the `src/index.tsx` to the following which will add the roboto
and material-icon fonts. It also removes the "strict" mode, which causes
issues when subscribing to ticking data.

```ts
import '@fontsource/roboto/300.css'
import '@fontsource/roboto/400.css'
import '@fontsource/roboto/500.css'
import '@fontsource/roboto/700.css'

import '@fontsource/material-icons'

import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App'

const root = createRoot(document.getElementById('root') as HTMLElement)
root.render(<App />)
```

Update `src/App.tsx` to include `CssBasline` which updates the browser's default
styles to be incline with material design.

```ts
import CssBaseline from '@mui/material/CssBaseline'

export default function App() {
  return (
    <div>
      <CssBaseline />
      Contents here
    </div>
  )
}
```

Check everything works by running `npm start`. The current version of cra asks you
to install `@babel/plugin-proposal-private-property-in-object` manually.

```bash
npm install @babel/plugin-proposal-private-property-in-object
```

Assuming everything is working, commit the changes.

```bash
git add .
git commit -m "Added material-ui"
```

## Step 4 - Setup GraphQL

Install the GraphQL package.

```bash
npm install @barejs/graphql-observable
```

We can test the GraphQL communication.

Add a `components` folder under `src` and create the file `src/components/BidAsk.tsx` with
the following content.

```ts
import { useEffect } from 'react'

import { graphqlObservableStreamClient as graphQL } from '@barejs/graphql-observable'

const GRAPHQL_URL = 'http://192.168.86.216:9009/graphql'

export default function BookTickerPage() {
  useEffect(() => {
    console.log('Requesting data')

    const symbols = ['btcusdt', 'ethusdt']

    const subscription = graphQL(
      GRAPHQL_URL,
      {},
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
      null
    ).subscribe({
      next: data => console.log(data),
      error: error => console.error(error),
      complete: () => console.log('done')
    })

    return () => subscription.unsubscribe()
  }, [])

  return <div>Book ticker page</div>
}
```

# Step 5 - Refactor the GraphQL API

Simplify the querying by creating a file `src/api.ts` with the following content.

```ts
import {
  graphqlObservableStreamClient as graphqlClient,
  GraphQLError
} from '@barejs/graphql-observable'

export interface GraphQLResponse {
  data: any
  errors: any
}

const GRAPHQL_URL = 'http://192.168.86.216:9009/graphql'

const noop = () => {}

export function queryGraphQL(
  query: string,
  variables: object,
  onError: (error: Error) => void,
  onNext: (response: GraphQLResponse) => void,
  onComplete: () => void = noop
) {
  const init: RequestInit = {}
  return graphqlClient(GRAPHQL_URL, init, query, variables, null).subscribe({
    next: value => {
      const response = value as GraphQLResponse
      if (response.errors) {
        onError(new GraphQLError(response.errors))
      } else {
        onNext(response)
      }
    },
    error: onError,
    complete: onComplete
  })
}
```

And update `src/components/BookTicker` to the following.

```ts
import React, { useEffect } from 'react'

import { queryGraphQL } from '../api'

export interface BookTickerPageProps {
  symbols: string[]
}

export function BookTickerPage: React.FC<BookTickerPageProps> = ({ symbols }) => {
  useEffect(() => {
    console.log('Requesting data')

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
      data => console.log(data)
    )

    return () => subscription.unsubscribe()
  }, [symbols])

  return <div>Book ticker page</div>
}
```

Change `src/App.tsx` to the following.

```ts
import CssBaseline from '@mui/material/CssBaseline'

import { BookTickerPage } from './components/BookTickerPage/BookTickerPage'

export default function App() {
  return (
    <div>
      <CssBaseline />
      <BookTickerPage symbols={['bnbusdt', 'btcusdt', 'ethusdt']} />
    </div>
  )
}
```