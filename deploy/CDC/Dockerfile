FROM confluentinc/cp-kafka-connect:latest

# Install Debezium PostgreSQL connector
RUN confluent-hub install --no-prompt debezium/debezium-connector-postgresql:latest

# Install Elasticsearch sink connector
RUN confluent-hub install --no-prompt confluentinc/kafka-connect-elasticsearch:latest

# Expose the REST port
EXPOSE 8083
