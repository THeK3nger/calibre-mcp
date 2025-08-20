# Calibre MCP

This is an experimental Calibre MCP working via Calibre native Content Server.

## Features

This MCP mostly wraps around `calibredb` so I plan to add all the features from it. Mainly:

- [x] Query the Calibre library.
- [x] Search Books.
- [x] Full Text Search.
- [x] Get Book's Metadata.
- [x] List/Edit Custom Columns.
- [ ] List/Edit Metadata.

... and then we will see.

## How to use

At the moment, this is a very development version. So, it is mostly focused for my workflow of running it directly from source. However, I am open to contributions in the "easy of use" direction. For instance, if you want to make a `Dockerfile` to run it via docker, you are more than welcome.

### Run it directly

1. Before we start, you need `python` 3.10 (or later) and `uv` installed on your system.

2. Download the source code.

```bash
git clone git@github.com:THeK3nger/calibre-mcp.git
cd calibre-mcp
```

3. Now we install the MCP into Claude Desktop with:

```bash
uv run mcp install server.py
```

4. Now, unless you run Calibre Content Server to the default url (`http://localhost:8080`) and your library ID is `Library`, you may have to configure two environment variables in the Claude Desktop configuration. So, let's open the `claude_desktop_config.json` (on macOS you can find it in `~/Library/Application Support/Claude/`, on Linux it should be in the `~/.config` folder).

5. Find the configuration for the Calibre MPC. It should look like this:

``` json
    "Calibre": {
      "command": "/opt/homebrew/bin/uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "/path/to/calibre-mcp/server.py"
      ]
    }
```

6. Now we can add the two environment variables. Replace `CALIBRE_BASE_URL` with your Content Server URL and `CALIBRE_LIBRARY_ID` with your library ID.

``` json
    "Calibre": {
      "command": "/opt/homebrew/bin/uv",
      "args": [
        "run",
        "--with",
        "mcp[cli]",
        "mcp",
        "run",
        "/path/to/calibre-mcp/server.py"
      ],
      "env": {
        "CALIBRE_BASE_URL": "http://localhost:8080",
        "CALIBRE_LIBRARY_ID": "Library"
      }
    }
```

7. That's it. Now you can enjoy the MCP server. Just make sure you started Calibre's Content Server.

## Important Notes

### Write Operations

Tools that perform editing operations (such as `setCustomColumn`) require the Calibre Content Server to be run with the `--enable-local-write` flag or have the corresponding setting enabled in Calibre's preferences. Without this setting, write operations will fail.

To enable local write access:
- **Command line**: Start the Content Server with `calibre-server --enable-local-write`
- **GUI**: In Calibre preferences, go to "Sharing over the net" and enable "Allow un-authenticated local connections to make changes" in the "Advanced" tab.

### Authentication

At the moment, this MCP server does not support authentication. If your Calibre Content Server requires authentication, you will need to configure it to allow unauthenticated access or modify the server code to include authentication credentials.

## Configuration with other clients

Of course, MCP are generic and you can configure them with clients other than Claude Desktop. For instance VSCode can automatically load the Claude Desktop configuration so that you can use the MCP server with Copilot. Other clients may have different configurations. Refer to their documentation for more info (or open a PR on the README and let's add more info here!)
