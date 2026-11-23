(1)
Aim: To implement a counter using React class components.
Program :

import React, { Component } from 'react';

class CounterClass extends Component {

  constructor() {
    super();
    this.state = { count: 0 };
  }

  increment = () => {
    this.setState({ count: this.state.count + 1 });
  };

  render() {
    return (
      <div>
        <h2>Counter: {this.state.count}</h2>

        <button onClick={this.increment}>
          Increment
        </button>
      </div>
    );
  }
}

export default CounterClass;

OUTPUT :
Counter:
[Increment]
Try clicking the button to see how the counter works!


===================================================================================================================
(2)
Aim: To handle and respond to button click events using JavaScript.
Program :

<!DOCTYPE html>
<html>

<head>
    <title>Click Event</title>
</head>

<body>

    <button onclick="handleClick()">Click Here</button>

    <p id="output"></p>

    <script src="click.js"></script>

</body>
</html>

#click.js

function handleClick() {
    document.getElementById("output").innerText =
        "You clicked the button!";
}


===================================================================================================================
(3)
Aim: To create a counter using React functional components and Hooks.
Program :

import React, { useState } from 'react';

function CounterFunctional() {

  const [count, setCount] = useState(0);

  return (
    <div>

      <h2>Counter: {count}</h2>

      <button onClick={() => setCount(count + 1)}>
        Increment
      </button>

    </div>
  );
}

export default CounterFunctional;

OUTPUT :
Counter:
[Increment]
Click to increase the counter.


===================================================================================================================
(4)
Aim: To fetch API data when the component mounts.
Program :

import React, { useState, useEffect } from 'react';

function FetchWithEffect() {

  const [data, setData] = useState(null);

  useEffect(() => {

    fetch('https://jsonplaceholder.typicode.com/posts/1')
      .then(res => res.json())
      .then(json => setData(json));

  }, []);

  return (
    <div>

      {data ? (
        <>
          <h4>{data.title}</h4>
          <p>{data.body}</p>
        </>
      ) : (
        <p>Loading...</p>
      )}

    </div>
  );
}

export default FetchWithEffect;

OUTPUT :
Display fetched post's title and body after loading delay.


===================================================================================================================
(5)
Aim: To pass data from a parent component to a child component using Props.
program :
import React from 'react';

function Child({ message }) {
  return (
    <p>Message from parent: {message}</p>
  );
}

function Parent() {
  return (
    <Child message="Hello from Parent!" />
  );
}

export default Parent;


OUTPUT :
Message from parent: Hello from Parent!




===================================================================================================================
(6)
Aim: To execute a side-effect script when serving a route.
Program :

const express = require('express');

const app = express();

app.get('/', (req, res) => {

    console.log('Hello, world! printed in server console');

    res.send('Check the server console.');

});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});

OUTPUT :
1. Browser output:
localhost:3000
Check the server console.
2. Server console output:
Server running on port 3000
Hello, world! printed in server console


===================================================================================================================
(7)
Aim: To interact with MySQL database from Express.js.
Program :

const express = require('express');
const mysql = require('mysql2');

const app = express();

const pool = mysql.createPool({
    host: 'localhost',
    user: 'youruser',
    password: 'yourpass',
    database: 'testdb'
});

app.get('/users', (req, res) => {

    pool.query('SELECT * FROM users', (err, results) => {

        if (err) {
            res.status(500).send(err);
        } else {
            res.json(results);
        }

    });

});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});

OUTPUT :
GET/user returns row from users table.



===================================================================================================================
(8)
To practice SQL structure creation using MySQL commands.
Program :

CREATE DATABASE school;

USE school;

CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    age INT
);


OUTPUT :
Database and table created in MySQL.



===================================================================================================================
(9)
Aim: To manipulate table data using INSERT and UPDATE commands in MySQL.
Program :

INSERT INTO students (name, age)
VALUES ('Alice', 20);

INSERT INTO students (name, age)
VALUES ('Bob', 22);

UPDATE students
SET age = 23
WHERE name = 'Bob';

OUTPUT :
Two records inserted: Bob's age updated.



===================================================================================================================
(10)
Aim: To demonstrate how to link an external JavaScript file to an HTML page.
Program :

<!DOCTYPE html>
<html>

<head>
    <title>Link JavaScript</title>
</head>

<body>

    <h1>Hello from HTML</h1>

    <script src="script.js"></script>

</body>
</html>


#script.js
console.log("JavaScript file linked successfully!");

OUTPUT : Hello from HTML
Open the browser console,and you will see :
JavaScript file linked successfully!

===================================================================================================================
#Browser Console (F12 → Console):
