FROM python:3.10-slim 
WORKDIR /app 
RUN apt-get update && apt-get install -y xorg-dev libglu1-mesa-dev 
RUN pip install evogym==2.0.0 
RUN pip install neat-python==0.92 imageio==2.37.3 dill==0.4.1 pathos==0.3.5
ADD . /app 
ENV PYTHONUNBUFFERED=1
CMD ["python", "sgr_main.py"]