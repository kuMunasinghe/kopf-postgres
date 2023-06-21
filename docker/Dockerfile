FROM python:3.10

RUN pip install kopf && pip install kubernetes 

RUN mkdir operator

WORKDIR /operator

COPY run.py . 

COPY docker-entrypoint.sh .

# add execute permission to docker-entrypoint script
RUN chmod 740 docker-entrypoint.sh

ENTRYPOINT /operator/docker-entrypoint.sh

# expose ports 
EXPOSE 8080 6443 443