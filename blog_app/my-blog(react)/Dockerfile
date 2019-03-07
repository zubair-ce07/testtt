FROM node:8.12.0
# set working directory
RUN mkdir -p /usr/apps/my-blog/front-end
WORKDIR /usr/apps/my-blog/front-end
# install and cache app dependencies
ADD package.json package-lock.json ./
RUN npm install
# add app
ADD . .
