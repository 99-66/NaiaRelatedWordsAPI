FROM python:3.6-slim

COPY . /app
ENV HOME=/app

# Build Argument Set
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ARG ELS_HOST=${ELS_HOST}
ARG ELS_USER=${ELS_USER}
ARG ELS_PASSWORD=${ELS_PASSWORD}
ARG ELS_TEXT_INDEX=${ELS_TEXT_INDEX}

# Env Set
ENV APP_ENV=production
ENV ELS_HOST=${ELS_HOST}
ENV ELS_USER=${ELS_USER}
ENV ELS_PASSWORD=${ELS_PASSWORD}
ENV ELS_TEXT_INDEX=${ELS_TEXT_INDEX}

# Timezone Set
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul

# Build
WORKDIR ${HOME}
RUN apt-get update \
&& apt-get install apt-utils tzdata -y  \
&& pip install --no-cache-dir -r requirements.txt

EXPOSE 8001

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
