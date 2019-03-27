$TTL 1h
dynamic.com. IN SOA ns1.dynamic.com. phil@test.com. (
                2 ;serial
                3h ;refresh
        1h ;retry
        1w ;expire
        1h ;negative caching ttl
)
dynamic.com. IN NS ns1.dynamic.com.
ns1 IN A 192.168.1.2
combine-record IN A 192.168.1.3