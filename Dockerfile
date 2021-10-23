FROM python:3.9
# File Author / Maintainer
MAINTAINER Patrick Tchankue
RUN printf "deb http://archive.debian.org/debian/ jessie main\ndeb-src http://archive.debian.org/debian/ jessie main\ndeb http://security.debian.org jessie/updates main\ndeb-src http://security.debian.org jessie/updates main" > /etc/apt/sources.list
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 8B48AD6246925553 7638D0442B90D010 CBF8D6FD518E17E1
RUN apt-get update && apt-get install -y build-essential

ENV APP_HOME /bellabooks
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

ADD requirements.txt $APP_HOME
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ADD . $APP_HOME
