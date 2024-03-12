#Using python
FROM python:3.9-slim

# Using Layered approach for the installation of requirements
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

#Copy files to your container
COPY . ./

EXPOSE 8050

#Running your APP and doing some PORT Forwarding
CMD ["python", "app.py"]



