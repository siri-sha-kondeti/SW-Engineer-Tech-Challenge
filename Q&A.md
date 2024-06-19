## 1. What were the reasons for your choice of API/protocol/architectural style used for the client-server communication?

### APIs chosen for the Development 
  1. FastAPI for Server Implementation 
  
  2. RESTful API for Communication

#### Reasons for Choosing
#### FastAPI:
it has Asynchronous Support, Performance (as FastAPI is one of the fastest Python Frameworks and High performance is essential for the real time system like this) So I have Chose the FastAPI, and it has Built-in validation and serialization so that the data received from client is properly formatted and validated.
#### RESTful API:
It uses standard HTTP methods like GET,POST,PUT and DELETE and status codes, making it easier to implement and maintain. REST API are stateless so that each request from the client to the server contains all the necessary information the server can fulfill the request. This fits well with the asynchronous nature of the task, as each data submission from the client can be processed independently. these APIs are designed to scale easily with increased load which is essential for a system that might need to handle a large number of DICOM series beging uploaded over the time.

### Protocol chosen for the Development
HTTP Protocol for Data Transmission
#### Reason for choosing:
With this protocol it is easy to add layers of security such as HTTPS which encrypts the data transmitted between the client and server so that we can protect sensitive personal and medical information of the patient. This Protocol also use of standard headers (like Authorization for access tokens), making it straightforward to implement security features like API key validation.

### Architectural Style for Client-Server Communication
The architectural style used for the client-server communication in this project is a RESTful architecture implemented using the FastAPI framework. So, this
architectural style, combined with security measures like HTTPS and authentication of API keys, helps secure and guarantee data transmissions with the availability of a simple, scalable, and flexible communication protocol for the project. This availability of an architectural style, coupled with security measures like HTTPS and authentication of API keys, makes this process secure and guarantees transmissions in a way that fulfills requirements regarding sensitive medical data in a real-world application.

## 2. As the client and server communicate over the internet in the real world, what measures would you take to secure the data transmission and how would you implement them?

The data transmission security becomes relevant mainly in real-world client-server communication where sensitive data, for example, medical data, is being communicated. Below are some such measures that can be taken to make sure that data transmission is secure and how to implement them.

**HTTPS:** It will ensure that the data is encrypted during its transmission and thus safe from eavesdropping and tampering.
- **Implementation:**
  - **Generate SSL/TLS certificates:** Get them from a trusted Certificate Authority (CA).
  - **Set up server to use HTTPS:** Update FastAPI server to use these certificates.
  - **Ensure the client is making requests over HTTPS.**

**API Key Authentication:** Server will only allow authorized clients to send their data to itself.
- **Implementation:**
  - **Create an API key:** The Client must include it in the request headers.
  - **API Key Verification at Server End:** The Server should verify the API key and only then proceed with processing any request.

**Data Encryption:** The data from the sensitive client, if any, may be encrypted for more secure transportation.
- **Implementation:**
  - Apply symmetric encryption like AES on data before transfer.
  - On receiving, this data can be decrypted at the server end.

These are, thus, parts of the excellent framework for security implementation when critical medical data passes to and fro between the client and server in a real-life application.



