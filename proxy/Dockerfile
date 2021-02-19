FROM ruby:3-slim

RUN bundle config --global frozen 1

WORKDIR /usr/src/app

COPY Gemfile Gemfile.lock ./
RUN bundle install

COPY . .

EXPOSE 8080

CMD ["./proxy.rb", "-p", "8080", "-o", "0.0.0.0"]
