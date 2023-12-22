# PyMsSQL with a Turbo
My own code to manage a connection to a Microsoft SQL Server in Python, built on top of pymssql.

## Why I did it
I had to work on a project that used MS SQL Server hosted on Azure. The loading times for a small SQL query were driving me insane, and I couldn't find anything that worked competently and matched my own requirements:
- Not starting a connection everytime a query was run, and then killing it immediately.
- Reusing the connection as much as possible.
- Having a cache for when users run exactly the same query on a specific time frame.

As such, this code tries to:
- Always reuse the connection if it hasn't been terminated by the remote server (this actually made the queries much faster).
- Use a cache, so that when users run the same query within a specific time interval, we don't overload our SQL Server, and return the results to the user much faster.

## Why I made it public
It worked very well on the flask project I created it for, and I thought it could be helpful for other people.

## What is missing?
I didn't add yet a scape for when the query is an INSERT or an UPDATE, but that is on my todo list and should be added soon.

I also believe that a connection pooling should be added, as currently we only use a single connection at a time. This decision was mainly based due to the low load the app this was built for is actually going to have.
