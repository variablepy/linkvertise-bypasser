getcontentquery = """query getContent($identifier: PublicLinkIdentificationInput!, $task_args: TaskArgument) {
  getContent(input: $identifier, task_args: $task_args) {
    ... on ContentAccessTaskSet {
      __typename
      tasks {
        __typename
        id
        ... on PremiumTask {
          __typename
          status
          id
        }
        ... on WaitTask {
          __typename
          id
          remainingWaitingTime
          status
          adsTotal
        }
        ... on AdTask {
          __typename
          id
          status
          payloadBag {
            taboola {
              session_id
              __typename
            }
            __typename
          }
          ads {
            ...AdsFragment
            __typename
          }
          adIndex
          adsTotal
        }
      }
    }
    ... on DetailPageTargetData {
      type
      url
      paste
      __typename
    }
    __typename
  }
}

fragment AdsFragment on CustomAdOffer {
  completion_token
  call_to_action
  countdown
  description
  provider
  title
  provider_additional_payload {
    taboola {
      available_event_url
      visible_event_url
      __typename
    }
    __typename
  }
  clickout_action {
    type
    ... on CustomAdOfferClickoutUrlAction {
      type
      clickout_url
      __typename
    }
    __typename
  }
  media {
    type
    ... on UrlMediaResource {
      content_type
      resource_url
      __typename
    }
    __typename
  }
  __typename
}"""

completetaskquery = """mutation completeTask($identifier: PublicLinkIdentificationInput!, $task_id: String!, $task_args: TaskArgument) {
  completeTask(input: $identifier, task_id: $task_id, task_args: $task_args) {
    id
    ... on AdTask {
      __typename
      id
      status
    }
    ... on PremiumTask {
      __typename
      status
      id
    }
    ... on WaitTask {
      __typename
      id
      status
      remainingWaitingTime
      adsTotal
    }
    __typename
  }
}"""