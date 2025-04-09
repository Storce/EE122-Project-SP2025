FROM python:3
ADD server.py server.py
ADD ../../requirement.txt requirement.txt
RUN pip install -r requirement.txt
EXPOSE 5000
ENTRYPOINT ["python3", "server.py"]
