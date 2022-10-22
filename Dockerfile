FROM python:3.10.7
WORKDIR /usr/src/tdsgndot
COPY . /usr/src/tdsgnbot
RUN pip install --user -r /usr/src/tdsgnbot/req.txt
CMD ["python", "main.py"]
