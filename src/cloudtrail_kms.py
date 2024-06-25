import boto3
from botocore.exceptions import ClientError
from botocore.config import Config
from datetime import datetime, timedelta
from loggerly import SimpleLogger

class GetCountCloudTrailEvents:

    def __init__(self, lookup: list = None, region: str = "us-east-1", delta_in_hours: int = 1):

        """
        Initializes the GetCountCloudTrailEvents class.

        Args:
            lookup (list, optional): A list of lookup attributes for CloudTrail events. Defaults to None.
            region (str, optional): The AWS region to search for CloudTrail events. Defaults to "us-east-1".
            delta_in_hours (int, optional): The time range in hours to search for CloudTrail events. Defaults to 1.

        Returns:
            None

        """

        self.delta_in_hours = delta_in_hours
        self.regions = [ region ]
        self.classname = 'GetCountCloudTrailEvents'
        self.logger = SimpleLogger(self.classname)

        if lookup is None:
            self.lookup = self._get_default_lookup()
        else:
            self.lookup = lookup

    def _get_time_range(self) -> dict:
        
        """
        Returns a dictionary containing the start and end time for CloudTrail lookup.

        Returns:
            dict: Dictionary with keys "StartTime" and "EndTime".
        """

        endtime = datetime.now()  # start and end time for CloudTrail lookup
        interval = timedelta(hours=self.delta_in_hours)
        starttime = endtime - interval

        return {
            "StartTime":starttime,
            "EndTime":endtime
        }

    def _get_default_lookup(self) -> list:
        
        """
        A function that returns the default lookup for cloudtrail.
        ref: https://docs.aws.amazon.com/kms/latest/developerguide/ct-decrypt.html

        Returns:
            list: A list of default lookup values for cloudtrail.
        """

        return [
            {
                'AttributeKey': 'EventName',
                'AttributeValue': 'Decrypt'
            },
            {
                'AttributeKey': 'EventSource',
                'AttributeValue': 'kms.amazonaws.com'
            }
        ]

    def get_count(self) -> int:

        """
        Retrieves the count of CloudTrail events that match the specified lookup attributes within the specified time range.

        Returns:
            int: The count of CloudTrail events that match the specified lookup attributes within the specified time range.
        """

        inputargs = self._get_time_range()
        inputargs["LookupAttributes"] = self.lookup

        for region in self.regions:
            try:
                cloudtrail = boto3.client("cloudtrail",
                                          config=Config(region_name=region))
            except ClientError as e:
                self.logger.warn(f"Error: {e}, region: {region}")
                continue

            # Fetch the CloudTrail events
            response = cloudtrail.lookup_events(**inputargs)

            if not response['Events']:
                count = []
            else:
                count = len(response["Events"])

            while 'NextToken' in response:
                response = cloudtrail.lookup_events(NextToken=response['NextToken'],
                                                    **inputargs)
                count += len(response['Events'])

            return count

    def print_count(self):
        
        """
        Print the count of cloudtrail lookup events found in the last delta_in_hours.

        This function retrieves the count of cloudtrail lookup events using the `get_count` method and prints a message
        indicating the number of events found in the last delta_in_hours.

        Parameters:
            self (object): The instance of the class.

        Returns:
            None
        """

        count = self.get_count()
        print(f"Found {count} cloudtrail lookup events in the last {self.delta_in_hours} hour(s).")

if __name__ == '__main__':

    main = GetCountCloudTrailEvents(lookup=None,
                                    delta_in_hours=1)

    main.print_count()