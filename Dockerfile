FROM python:3.6-alpine

# Create app directory
ADD . /app
WORKDIR /app

# Install app dependencies

RUN pip install -r requirements.txt
RUN pip install .
# Bundle app source
COPY src /app

EXPOSE 50022
CMD [ "my-twitter"]
