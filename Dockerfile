FROM python:3.12

WORKDIR /usr/www/work_time_app

COPY requirements.txt .
COPY start_app.sh .

COPY . /usr/www/work_time_app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

RUN chmod +x *.sh


CMD ["bash","start_app.sh"]
