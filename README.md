<p align="center"><img src="./backend/static/img/logo.png" width="256" /></p>

<h1 align="center">relay.md</h1>

<div align="center">
  <a href='./LICENSE'>
    <img src='https://img.shields.io/badge/License-AGPL_v3-blue.svg' alt='License' />
  </a>
</div>

Relay.md enables multiplayer [obsidian](https://obsidian.md), a note taking software for your personal knowledge base that does not come with any means to communicate notes.

The software in this repository represents the backend and website that offers an API and user interface. Integration with Obsidian itself requires the installation of [the relay.md plugin](https://github.com/relay-md/relay-md-obsidian-plugin).

# Getting Started

The software is configured in a way that allows deploying as microservices. The required services are:

 * `web`: This service provides the website where people can register, login and manage teams and topics
 * `api`: This service provides the application programming interface to the obsidian plugin and allows for posting, editing and deleting of notes and embeds.

You can start your local development environment using docker-compose:

    docker-compose up

# Contributing

If you encounter a bug, please file an [issue](https://github.com/relay-md/relay.md/issues) to let us know. Alternatively, please feel free to contribute a bug fix directly. If you are planning to contribute changes that involve significant design choices, please open an issue for discussion instead.

# Testing

Test are implemented using `pytest`. After configuring your virtual environment and installing the dependencies, you can run the unittests with

    python3 -m pytest

# License and Terms

The relay.md backend software is licensed under AGPLv3. The full license can be found [here](https://github.com/relay-md/relay.md/blob/master/LICENSE).
