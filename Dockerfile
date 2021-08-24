FROM openjdk:slim
COPY --from=python:3.6 / /

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt
# RUN wget https://github.com/allure-framework/allure2/releases/download/2.7.0/allure-2.7.0.zip
# RUN unzip allure-2.7.0.zip -d /bin/
# ENV PATH="/bin/allure-2.7.0/bin/:${PATH}"

EXPOSE 6000

CMD ["python", "./main.py"]