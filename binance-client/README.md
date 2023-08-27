# binance-client

This is a trivial client to demonstrate displaying data from binance via a python
server which presents the data as GraphQL.

## Usage

### Step 1 - Install The Packages.

```bash
binance-client $ npm install
```

### Step 2 - Update The Host IP Address

In the file `src/api.ts` change the following line to have your ip address.

```ts
const GRAPHQL_URL = 'http://192.168.86.216:9009/graphql'
```

We need to do this to satisfy CORS.

### Step 3 - Start The Python Server

See the README in the `binance-server` folder.

### Step 3 - Run The React Dev Server

Start the dev server.

```bash
npm start
```
