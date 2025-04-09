FROM python:3
ADD backend/single_server.py server.py
ADD backend/requirement.txt requirement.txt
RUN pip install -r requirement.txt
EXPOSE 5000
ENTRYPOINT ["python3", "server.py"]
