# Floy Software Challenge
This repository contains the necessary client-server-database files. The goal is to develop an end-to-end system that integrates with a PACS (Picture Archiving and Communication System) to receive DICOM files, extract information, and store the data in a SQLite database.

# Overview:
Receiving DICOM files from a PACS.
Extracting relevant information from the DICOM files.
Sending the extracted information to a server.
Storing the information in a database.
Architecture
Component Diagram

## The system is designed with the following components:

Client: Receives DICOM files from the PACS and extracts information.
Server: Provides an API to receive data from the client and store it in a database.
Database: Stores the extracted information in an Tabular Form.

## The sequence of operations is as follows:

Setup Instructions
## Prerequisites
Python 3.7 or newer
Docker
## Installing Dependencies
pip3 install -r requirements.txt

## Starting the Client
python client.py

## Starting the Server
python server.py

## Testing
To validate the implementation, run the test suite files that are in test folder.

## Architecture and Sequence Diagram 
![Floy_ Sequence_Diagram](https://github.com/siri-sha-kondeti/SW-Engineer-Tech-Challenge/assets/173000379/00f904cd-ef75-41df-90a1-0573ae2fb2b3)
