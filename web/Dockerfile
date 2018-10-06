FROM nginx:alpine

COPY mynginx.conf /etc/nginx/nginx.conf

COPY index.html /usr/share/nginx/html
COPY js /usr/share/nginx/html/js
COPY css /usr/share/nginx/html/css
COPY images /usr/share/nginx/html/images

#RUN sed -i -e 's#API_URL#http://routingcore/api#g' /usr/share/nginx/html/js/utils.js