version: '3.7'  # Vous pouvez ajuster la version ici si nécessaire
services:
  elasticsearch:
    image: docker.elastic.co/elasticsearch/elasticsearch:7.16.3
    container_name: elasticsearch
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false  
      - "ES_JAVA_OPTS=-Xms512m -Xmx512m"  
    ports:
      - 9200:9200
    volumes:
      - esdata:/usr/share/elasticsearch/data
 
  kibana:
    image: docker.elastic.co/kibana/kibana:7.16.3
    container_name: kibana
    environment:
      - ELASTICSEARCH_HOSTS=http://elasticsearch:9200
    ports:
      - 5601:5601
 
volumes:
  esdata:
    driver: local