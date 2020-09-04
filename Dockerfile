FROM fbiopereira/ssm-base-image-3-8-5:latest

COPY requirements.txt /tmp/requirements.txt

RUN pip3 install -r /tmp/requirements.txt && \
    rm -r /root/.cache
    
RUN apk add --no-cache libpcap

COPY configuration/nginx.conf /etc/nginx/
COPY configuration/flask-site-nginx.conf /etc/nginx/conf.d/
COPY configuration/uwsgi.ini /etc/uwsgi/
COPY configuration/supervisord.conf /etc/supervisord.conf
COPY configuration/filebeat.yml /filebeat
COPY scripts/start.sh /app/start.sh

RUN mkdir -p /mnt/videos_to_check
RUN chmod 777 -R /mnt/videos_to_check

RUN mkdir -p /var/log/app
RUN chmod 777 -R /var/log/app

RUN mkdir -p /app/temp/
RUN chmod 777 -R /app/temp/

COPY . /app
WORKDIR /app

#ARG ENVIRONMENT
#ENV ENVIRONMENT=$ENVIRONMENT
ENV ENVIRONMENT=production

RUN mkdir -p log
RUN chown -R nginx *
RUN chown -R nginx /app/start.sh
RUN chmod u+x /app/start.sh
RUN chmod go-w /filebeat/filebeat.yml


CMD ["/app/start.sh"]
