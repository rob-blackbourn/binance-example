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
