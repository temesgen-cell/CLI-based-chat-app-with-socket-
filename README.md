

# 💬 CLI Chat System: Real-Time TCP Chat

A simple, real-time, command-line interface (CLI) chat application built using Python's native **socket** library. This project serves as a foundational exercise in network programming, demonstrating basic **client-server architecture**, concurrent connection handling, and **TCP communication**.

-----

##  Features

  * **Client-Server Architecture:** Utilizes a dedicated server to relay messages between connected clients.
  * **Real-time Messaging:** Messages are broadcast to all connected users instantly.
  * **Multi-Client Support:** The server handles **concurrent connections** using Python's `[threading / asyncio]` module.
  * **Simple CLI Interface:** Clean, straightforward interface for chatting.
  * **Customizable:** Easy to extend with new commands or features.

-----

# 💬 CLI Chat System

A quick demo of the chat interface:

![Chat Interface Screenshot](assets/sockets-tcp-flow.1da426797e37.avif)

This image shows two clients communicating via the server.

-----

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You need to have **Python 3.x** installed on your system.

```bash
python --version
```

### Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/temesgen-cell/CLI-based-chat-app-with-socket- 
    cd CLI-based-chat-app-with-socket- 
    ```

2.  **No external libraries are required\!** This project uses only standard Python libraries (`socket`, `sys`, `threading`, etc.).

### Usage

The chat system requires running the server first, followed by one or more clients.

#### 1\. Start the Server

Open your first terminal window and run the server script, providing the desired IP and Port:

```bash
python server.py [HOST_IP] [PORT]
# Example:
python server.py 127.0.0.1 8888
```

#### 2\. Start a Client

Open one or more additional terminal windows to start clients, connecting to the server with a unique username:

```bash
python client.py [HOST_IP] [PORT] [USERNAME]
# Example:
python client.py 127.0.0.1 8888 Alice
```

Upon successful connection, the client will display a welcome message, and you can start typing:

```
Welcome, Alice! Start chatting.
>
```

-----

## Demo

A quick visual of the chat interface showing two clients communicating via the server.

-----

##  Project Structure

The repository is structured into two main components:

| File | Description |
| :--- | :--- |
| `server.py` | The main script that creates the **listening socket**, manages concurrent client connections, and handles message **broadcast** logic. |
| `client.py` | The script that creates the **connecting socket**, handles user input, and continuously **listens** for incoming messages from the server. |
| `README.md` | This file. |
| `LICENSE` | The license file for the project (e.g., MIT). |

-----

## 🧠Core Concepts & Technology

This project heavily relies on fundamental networking concepts implemented in Python:

### TCP Sockets

  * Uses **`AF_INET`** (IPv4) and **`SOCK_STREAM`** (TCP) for reliable, **connection-oriented** communication.
  * **Server:** Implements the core socket functions: `bind()`, `listen()`, and `accept()`.
  * **Client:** Implements the `connect()` function.

### Concurrency

  * The server uses Python's `[threading / asyncio]` module to ensure it can **simultaneously** handle messages from all connected clients without blocking the main event loop.
  * Each client connection is typically managed by a separate **thread** or **task**.

### Byte Handling

  * Data is sent and received over sockets as raw **bytes**.
  * The application handles the necessary conversion: **encoding** (`.encode('utf-8')`) of outbound text and **decoding** (`.decode('utf-8')`) of incoming bytes.