from clickhouse_driver import Client

client = Client(
    host='clickhouse-server',
    port=9000,
    user='default',
    password='admin',
    database='default'
)

