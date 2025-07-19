# Calibre MCP

This is an experimental Calibre MCP working via Calibre native Content Server.

## Features

This MCP mostly wraps around `calibredb` so I plan to add all the features from it. Mainly:

- [x] Query the Calibre library.
- [ ] Search Books.
- [ ] Full Text Search.
- [ ] Add/Remove Saved Searches.

... and more. 

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
  }
```

7. That's it. Now you can enjoy the MCP server. Just make sure you started Calibre's Content Server.

## Configuration with other clients 

Of course, MCP are generic and you can configure them with clients other than Claude Desktop. For instance VSCode can automatically load the Claude Desktop configuration so that you can use the MCP server with Copilot. Other clients may have different configurations. Refer to their documentation for more info (or open a PR on the README and let's add more info here!)
