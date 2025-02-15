FROM python:3.8.0
LABEL maintainer="Aji Wuryanto <aji.wuryanto@ui.ac.id>"
RUN apt-get update
RUN apt-get install -y python3-dev python3-pip nginx
RUN pip3 install uwsgi
COPY ./ ./app
WORKDIR /app
RUN pip3 install -r requirements.txt
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
ENV FLASK_APP=SISUKIT
ENV FLASK_ENV=development
EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"]
