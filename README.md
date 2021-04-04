# Guessing-Game
Guessing game web-application using Flask and MongoDB for Database Systems for Software and Knowledge Engineers.

## Cloning and Installation
* Install [Docker(with Docker Compose)](https://docs.docker.com/desktop/)
* Clone the project in command line.
    ```
    > git clone https://github.com/jeanyjean/guessing-game.git
    ```

## Getting Started
1. Change directory to where the project is.
    ```
    > cd guessing-game
    ```
2.  Run Docker Compose and the web application.
    ```
    > docker-compose up -d
    > docker-compose logs -f --tail 10 web
    ```
3. Access this link with your web browser. 
    * http://localhost/
4. Close the web application when you are done.
    ```
    > docker-compose down -v
    ```

Purich Trainorapong 6210545581