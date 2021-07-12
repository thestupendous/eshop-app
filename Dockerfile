FROM python
COPY . /e-commerce-app/
WORKDIR /e-commerce-app/
RUN pip3 install -r requirements/requirements.txt
CMD ["python3","app.py"]


EXPOSE 5005
