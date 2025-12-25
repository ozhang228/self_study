# HTTP Server Built in Python

- HTTP server to interact with files in the data/ directory.
- Built on top of TCP sockets
- Multithreaded with a listener thread and a variable number of worker threads
- Built to understand the HTTP protocol better.

## Features

### Threading

- [ ] Basic Support (main thread + other threads to answer one request)
- [ ] Persistent Connections + Connection Header support

### Supported Versions

- [x] HTTP/1.1
  - Following [RFC 2616, Section 5](https://datatracker.ietf.org/doc/html/rfc2616#section-5)
- [ ] HTTP/2
- [ ] HTTP/3

### Supported Methods

- [ ] **OPTIONS**: Gets information about what methods are allowed for the server
- [ ] **HEAD**: Gets information about the resource (as if a get request but without the body)
- [x] **GET**: Gets the contents of a file in the data directory if it exists.
- [ ] **POST**: Creates or overwrites the contents of a file in the data directory
- [ ] **PUT**: Updates a file in the data directory if it exists (idempotent)
- [ ] **DELETE**: Deletes a file in the data directory if it exists

### Request Parsing

**Parts**

- [x] Request-Line
- [ ] General-Headers
- [ ] Request-Headers
- [ ] Entity-Headers
- [ ] Query Params

### Responses

- [x] Basic Implementation
- [ ] Generate Response Headers

## Installation

- **Run Tests**

```bash
make test
```

- **Run Server**

```bash
uv run main.py
```
