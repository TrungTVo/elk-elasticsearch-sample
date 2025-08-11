# Sample Demo Logstash

Build Docker image

```
docker build -t trungtvo/custom-logstash:1.0 .
```

Create and run container

```
docker run --rm -it -p 5044:5044 -p 9600:9600 \
    -v ./logstash/config/:/usr/share/logstash/config/ \
    -v ./logstash/pipeline/:/usr/share/logstash/pipeline/ \
    -v ./workspace_data/:/usr/share/logstash/workspace_data/ \
    --name my-logstash-ctn \
    trungtvo/custom-logstash:1.0
```

Ports:

- 5044: filebeat
- 9600: node API calls

Access the container

```
docker exec -it my-logstash-ctn /bin/bash
```

Check pipeline settings

```
curl -X GET 'localhost:9600/_node/pipelines?pretty'
```

Should be able to access this endpoint from `localhost` on local browser or POSTMAN of host machine (because of `http.host: '0.0.0.0'`)

Output:

```
{
  "host" : "a48a589903f1",
  "version" : "8.12.0",
  "http_address" : "0.0.0.0:9600",
  "id" : "2aafdfa3-3306-423b-ab4a-4f6f622de689",
  "name" : "a48a589903f1",
  "ephemeral_id" : "ad02d52c-3652-43b2-bbad-021de33d76c7",
  "status" : "green",
  "snapshot" : false,
  "pipeline" : {
    "workers" : 4,
    "batch_size" : 125,
    "batch_delay" : 50
  },
  "pipelines" : {
    "my-logstash-pipeline_1" : {
      "ephemeral_id" : "d0ec6064-b422-434e-a4d3-2340083794ec",
      "hash" : "2f05e30997c57f9388420db5a2cbb...",
      "workers" : 4,
      "batch_size" : 125,
      "batch_delay" : 50,
      "config_reload_automatic" : false,
      "config_reload_interval" : 3000000000,
      "dead_letter_queue_enabled" : false
    }
  }
}
```

Here, `my-logstash-pipeline_1` is the name of the pipeline configured from `pipelines.yml` file. Pipeline is written with simple `stdin` as input, and the output is the log that is saved into specified file path: `/usr/share/logstash/workspace_logs/elk-output.log`.

When running the container, start typing in the terminal as `stdin`, check the `workspace_logs/elk-output.log` file and should see the result.

```
cat workspace_logs/elk-output.log
```

Result

```
{"@timestamp":"2024-02-05T00:24:01.785423076Z","message":"hello world...","event":{"original":"hello world..."},"host":{"hostname":"a48a589903f1"},"@version":"1"}

{"@timestamp":"2024-02-05T00:25:35.999564841Z","message":"hi trung","event":{"original":"hi trung"},"host":{"hostname":"a48a589903f1"},"@version":"1"}
```
