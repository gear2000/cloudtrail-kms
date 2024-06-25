#!/usr/bin/env python

import json
from cloudtrail_kms import GetCountCloudTrailEvents

def handler(event, context): 
    
    """
    Handles the event and context passed to the Lambda function.

    Args:
        event (dict or str): The event data passed to the Lambda function.
        context (object): The context object passed to the Lambda function.

    Returns:
        dict: A dictionary containing the response status code and the body of the response.

    """

    if not isinstance(event,dict):
        try:
            event = json.loads(event)
        except:
            print("")
            print("could not json loads to dictionary")
            print("")

    # this is sns trigger
    if "Records" in event:
        try:
            message = json.loads(event['Records'][0]['Sns']['Message'])
        except:
            message = event
    else:
        message = event

    # lookup for kms decrypt events in cloudtrail
    lookup = [
        {
            'AttributeKey': 'EventName',
            'AttributeValue': 'Decrypt'
        },
        {
            'AttributeKey': 'EventSource',
            'AttributeValue': 'kms.amazonaws.com'
        }
    ]

    # you can overide the delta in hours with the sns message
    delta_in_hours = int(message.get("delta_in_hours",1))

    main = GetCountCloudTrailEvents(lookup,
                                    delta_in_hours=delta_in_hours)

    count = main.get_count()
    print(f'kms decrypt events count "{count}" in last {delta_in_hours} hour')

    return {'statusCode': 200,
            'body': json.dumps({
                "count": count}
                )
            }