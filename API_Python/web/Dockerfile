FROM python
RUN apt update 
RUN apt install -y wget  
WORKDIR /tmp 
RUN  wget https://r.mariadb.com/downloads/mariadb_repo_setup
RUN chmod +x mariadb_repo_setup
RUN ./mariadb_repo_setup
RUN apt update 
RUN apt install -y  libmariadb3 libmariadb-dev
RUN pip install  fastapi uvicorn SQLAlchemy PyMySQL mariadb httpx

RUN mkdir -p /web/api 
WORKDIR /web/api 
COPY code/*  .
EXPOSE 8081
CMD ["uvicorn", "app:app" ,"--reload" ,"--port" ,"8081" ,"--host", "0.0.0.0"]
