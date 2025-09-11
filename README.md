# perses


## Download & install cli
https://github.com/perses/perses/releases

```
docker network create perses-net

docker run -d --name prometheus --rm --network perses-net -p 9092:9090 prom/prometheus

docker run -d --name grafana --rm --network perses-net -p 3002:3000 grafana/grafana-oss

docker run --name perses --rm -p 127.0.0.1:8090:8080 --network perses-net -v config.yaml:/q/config.yaml persesdev/perses
```
Info
```
# test query
docker run --rm --network perses-net curlimages/curl 'http://prometheus:9090/api/v1/query?query=prometheus_http_requests_total'

Perses server on 8090
Prometheus server on 9092
Grafana server on 3002
Perses access to the Prometheus with URL: http://prometheus:9090/ (Choose Proxy)
```

## Basic Commands
```
percli login http://localhost:8090
percli whoami
percli apply -f basics/project.json
percli get projects

# Create the datasource first
percli apply -f basics/initial_dashboard.json
percli get dashboards -p pp
```

## Migration Commands
```
# This grafana_sample.json dashboard was manually created on this(12.1.1) grafana ui.
percli migrate -f basics/grafana_sample.json --project pp --online -o json > basics/migrated_grafana_sample.json
percli apply -f basics/migrated_grafana_sample.json


percli migrate -f migration/grafana8_mongo_pod.json --project pp --online -o json > migration/new.json
Error: unable to decode the response body. Error name cannot be empty
```


## Clean up
`docker stop prometheus grafana perses`
