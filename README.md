# Elasticsearch and Kibana

Run Docker Compose

```
docker compose up
```

## Elasticsearch Container

### For ES Security settings:

Go inside ES container

```
docker exec -it es01 /bin/bash
```

Inside ES container, check default user of ES container

```
id
```

(OR can check directly using `docker exec -it es01 id`)

By default, ES container should not run as `root` user due to security reasons, thus default user is `elasticsearch`. Output:

```
uid=1000(elasticsearch) gid=0(root) groups=0(root)
```

Note that for accessing Kibana, default user is `elastic`, the password and an enrollment token for this user can be reset for Kibana as follow:

```
$ /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic
$ /usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana
```

Export the password into ENV variable in the shell/bash (Or store in `.env` file)

```
export ELASTIC_PASSWORD="your_password"
echo $ELASTIC_PASSWORD
```

In the host, we can manually set this `ELASTIC_PASSWORD` as an environment variable and then run `docker compose up`. This will pass this value into environment variables defined in ES container of `docker-compose.yml`. Once ES container starts, `ELASTIC_PASSWORD` will also be accessible inside ES container as well.

Check the ES node info

```
curl --cacert config/certs/http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:9200
```

Or to access this URL endpoint from the host, do following:

Copy `http_ca.crt` from ES container to current workspace of the host

```
docker cp es01:/usr/share/elasticsearch/config/certs/http_ca.crt ./elasticsearch
```

This will copy `http_ca.crt` from ES container into `./elasticsearch` folder

Next, also export `ELASTIC_PASSWORD` in the host as well, then run `curl` in the host:

```
curl --cacert ./elasticsearch/http_ca.crt -u elastic:$ELASTIC_PASSWORD https://localhost:9200
```

## Kibana Container

Once Kibana server starts, go to `http://localhost:5601/`

It will ask for enrollment token, which is generated above from ES container. To regenerate it, run this command again in ES container:

```
/usr/share/elasticsearch/bin/elasticsearch-create-enrollment-token -s kibana
```

Copy this token and paste it in Kibana UI.

In case Kibana server asks for verification code, do this:

Go inside Kibana container

```
docker exec -it kib01 /bin/bash
```

Run:

```
/usr/share/kibana/bin/kibana-verification-code
```

Copy this code and paste it in Kibana UI.

Then it will ask for username (default as `elastic`) and password.
Password can be regenerated as mentioned above in ES container:

```
/usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic
```
