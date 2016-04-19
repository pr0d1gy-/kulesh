FROM python:3.4-slim


RUN groupadd user && useradd --create-home --home-dir /home/user -g user user
COPY . /home/user/worker

RUN chown user:user /home/user -R

WORKDIR /home/user/worker

RUN pip3 install --no-cache-dir -r requirements.txt
RUN python3 -m flake8 .

USER user
CMD ["celery", "-A", "tasks", "worker", "--loglevel=info"]
