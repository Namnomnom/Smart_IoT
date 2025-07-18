import argparse
from datetime import datetime
import influxdb_client 
from influxdb_client.client.write_api import SYNCHRONOUS


def main(url, org, bucket, token):
    try:
        # instantiating client
        client =influxdb_client.InfluxDBClient(url=url, token=token, org=org)
        # instantiating a write client
        write_api = client.write_api(write_options=SYNCHRONOUS)
        # creating a data point
        point = influxdb_client.Point("sensor1").tag("type","temperature").field("reading", 30)
        # writing data point to influxdb
        write_api.write(bucket=bucket, org=org, record=point)
        print(f"Punkt wurde erstellt: {point}")
        client.close()
        print("Influxdb client closed")
    except Exception as e:
        print(f"Fehler taucht auf: {e}")

def parse_args():
    """Parse the args."""
    parser = argparse.ArgumentParser(description='example code to play with InfluxDB')
    parser.add_argument('--url', type=str, required=False,
                        default='http://localhost:8086',
                        help='hostname INCLUDING port for local installations, EXCLUDING port for cloud services')
    parser.add_argument('--bucket', type=str, required=False, default='smart-iot',
                        help='bucket to use for writing data')
    parser.add_argument('--org', type=str, required=False, default='Gruppe_01',
                        help='organization name as configured in InfluxDB UI')
    parser.add_argument('--token', type=str, required=False,
                        default='-Z8Px5qfHrg52MmKUgBmGz0i2KhsLyg48_WV5PmEg7W3XLLacgY7I28MAFiG1iskJ4w9dL44s6N1eqPToZCQ9A==',
                        help='API token generated in the InfluxDB UI')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    main(url=args.url, org=args.org, bucket=args.bucket, token=args.token)
