from influxdb_client import InfluxDBClient


def test_main(url, org, bucket, token):
    query = 'from(bucket: "' + bucket + '") \
      |> range(start: -1m) \
      |> filter(fn: (r) => r["_measurement"] == "sensor1") \
      |> filter(fn: (r) => r["_field"] == "reading") \
      |> filter(fn: (r) => r["type"] == "temperature") \
      |> aggregateWindow(every: 10s, fn: mean, createEmpty: false) \
      |> yield(name: "mean")'

    query_api = InfluxDBClient(url=url, token=token, org=org).query_api()
    result = query_api.query(org=org, query=query)
    results = []
    for table in result:
        for record in table.records:
            results.append(record.get_value())
    assert len(results) > 0
    print('sensor readings: ' + str(results))
