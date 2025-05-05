Title: Configuring a dev environment for Phoenix library development
Date: 2025-05-05
Status: published
Tags: phoenix, elixir

The great tooling around Elixir makes it easy to publish reusable bits of code as packages on the [hex](https://hex.pm/) registry.
Mix makes it easy to create new library project with `mix new`, and [publishing to hex](https://hex.pm/docs/publish) is simple with some configuration and running `mix hex.publish`.
Conversely, Phoenix projects are created with a great developer experience, featuring live reload and automatic code compilation.

However, if you want to develop a new package for use with Phoenix, such as a component library, LiveView `on_mount` plugin, or any other piece of shared code, then the DX story isn't so great out of the box.
If you're developing your package in one dir that's set up to publish, and testing it with a separate Phoenix project, you won't have live reload or auto code reloading by default.

This is a quick guide on a few ways I've found to configure Phoenix that makes developing a package much nicer, and enables quick reactivity and live reloading while developing.
Read on for some explanation behind how Phoenix does code and live reloading, or skip to one of these solutions to bootstrap your project with.

- **[Option 1](#option-1-sibling-projects)**: Creating two "sibling" projects, your package and a Phoenix project, side by side in the same parent directory. (Similar to a [poncho project](https://embedded-elixir.com/post/2017-05-19-poncho-projects/).)
2. **[Option 2](#option-2-a-subdir-phoenix-project)**: Creating a Phoenix project as a subdir inside your package dir, all as a monorepo.
3. **[Option 3](#option-3-umbrella)**: Using an umbrella project and publishing your library straight from its "app/" subdirectory. (Not recommended!)

# Understanding the Phoenix Developer Experience

There are two modules that give us the live reload experience when developing Phoenix applications, so that changes to source files appear in the browser without having to restart our server or reload the page.

## The Code Reloader

The first is [`Phoenix.CodeReloader`](https://hexdocs.pm/phoenix/Phoenix.CodeReloader.html), which is included in the `:phoenix` package.
This is a Plug that you can see in your "my_app_web/endpoint.ex" file as `plug Phoenix.CodeReloader`.
Whenever it handles a request, it uses mix to (re)compile your app before processing the rest of the plug pipeline.

It's important to note a few things:

- This only recompiles elixir code (`.ex` and `.*eex` files for example), similar to running `recompile` in `iex`.
  It will not recompile assets such as CSS or JS, which should be done by your asset tools like `esbuild` and `tailwind`.
- This will not recompile dependencies listed in your "mix.exs".
- This will only recompile things when it gets a request, it does not happen as soon as you save the source file.
- By default, it will only recompile your `:my_app` app (unless you're in an umbrella in which case it will recompile all apps in your "apps/".)
- By default, in a new Phoenix app, this is only enabled in the `dev` mix environment.
  It is possible to enable it in `prod`, but it requires `:mix` being available.
  See [the source code](https://github.com/phoenixframework/phoenix/blob/v1.7.21/lib/phoenix/code_reloader/server.ex#L198-L203) for a hint.

[Buried deep in the docs](https://hexdocs.pm/phoenix/Phoenix.CodeReloader.html#reload/2) is a clue how we can configure `Phoenix.CodeReloader` to recompile any app whenever it gets a request.
This functionality was probably created to serve umbrella apps, but even if we're not running in an umbrella, we can use it to configure any app in our BEAM server to be reloaded on request.
I'll go into more detail below in one of the demonstrated options, but in short, just give it a list of apps you want to recompile in "config/dev.exs":

```elixir
# Configure Phoenix.CodeReloader to reload my_library as well as this application on every request
config :my_app, MyAppWeb.Endpoint, reloadable_apps: [:my_app, :my_library]
```

After this, you should see

```
==> my_library
Compiling 1 file (.ex)
Generated my_library app
```

in your logs whenever you make a request and there has been a change in the `:my_library` app.

## The Live Reloader

The second piece of the puzzle is [`Phoenix.LiveReloader`](https://hexdocs.pm/phoenix_live_reload/Phoenix.LiveReloader.html) which is contained in the `:phoenix_live_reload` package.
This uses the `:file_system` package to monitor changes to files on disk and then notify the browser when it detects changes.
You can see this in your "my_app_web/endpoint.ex" file as:

```elixir
socket "/phoenix/live_reload/socket", Phoenix.LiveReloader.Socket
plug Phoenix.LiveReloader
```

A few notes about this module:

- This works for any files that change, as long as it matches the list of patterns. So css, js, images, etc, as well as elixir and template files.
- It works with the browser by injecting an iframe into every page served by Phoenix that contains custom JS to connect back to the server via a Phoenix Channel websocket connection.
- When a file changes, a message is pushed to the iframe code. If it's CSS, then it will attempt to inject it into the existing DOM. Otherwise, it will force a page reload.
- This is only for dev environments, and should never be used in production.

Again, [buried deep in the docs](https://hexdocs.pm/phoenix_live_reload/Phoenix.LiveReloader.html#module-configuration) is a note about configuring `Phoenix.LiveReloader` to work with umbrella apps that we can use to configure it for broader use in non-umbrella apps.
Nowhere else can I find the `:dirs` option documented, and that's probably because the value of it is passed directly to the `:file_system` module.
[The docs](https://hexdocs.pm/file_system/FileSystem.html#start_link/1) for `FileSystem.start_link/1` tell us that it's the list of directories to monitor.
The default is to watch `[""]` which `FileSystem` just interprets as the current working dir (cwd).

So if you want to watch more than one directory, such as your app and a dependency, that can be done with this, for example:

```elixir
# Configure Phoenix.LiveReloader to watch the CWD and `my_library` paths for file changes
config :phoenix_live_reload, :dirs, ["", "../my_library"]
```

This will cause `FileSystem` to monitor all changes in the current directory as well as a sibling "my_library/" directory.
However, in a new phoenix project, notifications are filtered so the browser doesn't reload unless a source file for our app is modified.
You wouldn't want your browser constantly reloading every time some temporary, build or cache files changed, after all.
The default config looks something like this:

```elixir
# Watch static and templates for browser reloading.
config :my_app, MyAppWeb.Endpoint,
  live_reload: [
    patterns: [
      ~r"priv/static/(?!uploads/).*(js|css|png|jpeg|jpg|gif|svg)$",
      ~r"priv/gettext/.*(po)$",
      ~r"lib/my_app_web/(?:controllers|live|components|router)/?.*\.(ex|heex)$",
    ]
  ]
```

It's important to note that when `Phoenix.LiveReloader` gets a notification of a file changing in any of the configured `:dirs`, the path given to it will be an absolute path.
So if we want to notify the browser when any file changes in our "../my_library" dir that we added above, then we just have to add this pattern: 

```elixir
~r"lib/my_library.*(ex|heex)$"
```

This will match any path ending with this pattern, such as "/path/to/my_library/lib/my_library.ex".

!!! accent "Debugging tip"
    If you're having trouble with your patterns, you can add some debug prints to "deps/phoenix_live_reload/lib/phoenix_live_reload/channel.ex" in the `handle_info({:file_event, ...}, ...)` function, then force recompile it with `mix deps.compile --force phoenix_live_reload`.
    
    This function is called by `FileSystem` every time it detects a changed file, and it's here where the server pushes a message to the browser.

# Example Setups

Now let's look at 3 different ways of configuring a development setup.
In each example our goal is to be able to publish a module called `MyLibrary` in a package named `:my_library`.
The hex package format basically requires a "mix.exs" with a few keys defined, and a list of dependencies that are required by your package.
These dependencies will be installed along with your package when someone does a `mix deps.get` after adding your package to their list of dependencies, so you should be careful with these dependency requirements.
See the [hex publishing guide](https://hex.pm/docs/publish) for more information than we'll cover here.

## Option 1: Sibling projects

In this scenario, we'll have a "my_library/" dir in the same parent directory as a "my_app/" Phoenix project to develop with.
So the two directories will be siblings, or side-by-side.

Pros:

- Your package directory will be clean of anything not directly related to it.
- You can publish your Phoenix project as a separate git repository for other people to check out.
- You can open these two projects in two different IDEs or text editors, and it's less likely to confuse your LSP.

Cons:

- You have to open two separate IDEs, or configure an overall Workspace to edit both projects in the same IDE.
- You have to commit changes to both git repositories separately, making synchronization of the two a little more involved.
- Other developers have to clone both repos to set up their dev environment, and update both when there are changes.

### Create the library `MyLibrary`

1. Change to the parent dir you want both projects to live in, such as "~/projects".
1. Create a new mix project with `mix new my_library`.
1. Change to the new dir with `cd my_library`.
1. Add `:phoenix_live_view` as a dependency to "mix.exs" so we can use `Phoenix.Component`.
   We'll use the spec `~> 1.0` to say our library works with any version of LiveView that is `>= 1.0.0 and < 2.0.0`.
```elixir
defp deps do
  [
    {:phoenix_live_view, "~> 1.0"}
  ]
end
```
1. Run `mix deps.get`
1. Edit "lib/my_library.ex" to be:
```elixir
defmodule MyLibrary do
  use Phoenix.Component

  def hello(assigns) do
    ~H"""
    <div>
      Hello, <%= @name %>!
    </div>
    """
  end
end
```
1. Edit "mix.exs" to add required hex package info in the main `project/0` function:
```elixir
def project do
  [
    app: :my_library,
+   description: "A library of Phoenix LiveView components",
    version: "0.1.0",
    elixir: "~> 1.18",
    start_permanent: Mix.env() == :prod,
    deps: deps(),
+   package: [
+     licenses: ["MIT"],
+     links: %{"GitHub" => "https://github.com/myuser/my_library"}
+   ]
  ]
end
```
1. Run `mix hex.build` to make sure that it will build a package tarball without error.

### Create the phoenix app `MyApp` / `MyAppWeb`

1. Change back to the parent directory (e.g. "~/projects") that "my_library/" is in with `cd ..`.
1. Create a new Phoenix project with `mix phx.new my_app`.
   Customize with whatever switches you want (e.g. `--no-ecto`, `--no-mailer`, etc).
   Say yes to "Fetch and install dependencies?".
1. Change to the new dir with `cd my_app`.
1. Add the library to the list of deps in "mix.exs" as a relative path.
  This will tell mix to use our sibling library instead of trying to fetch it from hex.pm.
```elixir
defp deps do
  [
    {:my_library, path: "../my_library"}
  ]
end
```
1. We'll create a new action in the default `PageController` just to test with. In "lib/my_app_web/controllers/page_controller.ex" create a new function:
```elixir
def hello(conn, %{"name" => name}) do
  render(conn, "hello.html", name: name)
end
```
1. Create the template "lib/my_app_web/controllers/page_html/hello.html.heex" to go along with this, which is where we're going to call our new `hello` component from `MyLibrary`:
    - **Phoenix < 1.8**
      ```elixir
      <MyLibrary.hello name={@name} />
      ```
    - **Phoenix >= 1.8**
      ```elixir
      <MyAppWeb.Layouts.app flash={@flash}>
        <MyLibrary.hello name={@name} />
      </MyAppWeb.Layouts.app>
      ```
1. Add this new action to your router, right below the one for `:home`:
```elixir
get "/hello/:name", PageController, :hello
```
1. Start up Phoenix with `mix phx.server` (or `iex -S mix phx.server` if you prefer.)
1. Navigate to [http://localhost:4000/hello/bob](http://localhost:4000/hello/bob).
   You should see "Hello, bob!".

### Configuring Phoenix for Live Reloading

At this point you should have a working page that uses the function component from your library.
However, make any kind of change to the function component in "my_library/lib/my_library.ex" and you'll notice a couple problems.

1. The browser doesn't reload on its own when you make a change.
2. Even hitting reload doesn't cause the change to show up.
3. Only stopping and starting the server will make the change appear in the browser.

So first let's get `Phoenix.CodeReloader` working so that `MyLibrary` is recompiled when it changes and the server gets a request.
This is as easy as adding this to our "my_app/config/dev.exs".

```elixir
# Configure Phoenix.CodeReloader to reload my_library as well as this application on every request
config :my_app, MyAppWeb.Endpoint, reloadable_apps: [:my_app, :my_library]
```

Restart your Phoenix server, make another change to "my_library/lib/my_library.ex", then refresh your browser and you should see the change appear, and a line about compiling "my_library" in your console.

Now that's done, let's get the browser to do the refreshing automatically, by configuring `Phoenix.LiveReloader`.
Again, in "my_app/config/dev.exs" add this line:

```elixir
# Configure Phoenix.LiveReloader to watch the CWD and `my_library` paths for file changes
config :phoenix_live_reload, :dirs, ["", "../my_library"]
```

This will cause `Phoenix.LiveReloader` to now watch our sibling "../my_library" directory in addition to the phoenix "my_app" directory.
However, it will most likely be filtering out these notifications, so we'll need to also add a line to the patterns so that it includes these changes as valid.

```elixir
# Watch static and templates for browser reloading.
config :my_app, MyAppWeb.Endpoint,
  live_reload: [
    patterns: [
      ~r"priv/static/(?!uploads/).*(js|css|png|jpeg|jpg|gif|svg)$",
      ~r"priv/gettext/.*(po)$",
      ~r"lib/my_app_web/(?:controllers|live|components|router)/?.*\.(ex|heex)$",
+     ~r"my_library/lib/.*(ex|heex)$"
    ]
  ]
```

Restart your Phoenix server one last time, again make a change to "my_library/lib/my_library.ex", and as soon as you save you should see the browser refresh and the change appear on its own.
If you don't, then recheck these steps and also review the sections above on [`Phoenix.CodeReloader`](#the-code-reloader) and [`Phoenix.LiveReloader`](#the-live-reloader)

### Bonus: Dynamically referencing the `:my_library` dependency

In the example above, we just hard-coded the path to `MyLibrary` in the "my_app/mix.exs" file.

```elixir
defp deps do
  [
    {:my_library, path: "../my_library"}
  ]
end
```

This is probably fine if only you or your team will using the "my_app/" project.
However, if you want to also publish "my_app/" as a demonstration of your library, for other people to clone, then we can do better.

#### Check for the existence of the sibling directory

Instead of just assuming "../my_library/" will exist, we can check for it, then use a relative path.
But if it doesn't exist, we can instead configure it as a normal hex package.
So if someone checks out "my_app/" but not "my_library/", then it will just pull the latest version from hex.pm.

First define a new function in "my_app/mix.exs".

```elixir
defp my_library() do
  if File.exists?(Path.expand("../my_library/mix.exs", __DIR__)) do
    {:my_library, path: Path.expand("../my_library", __DIR__)}
  else
    {:my_library, ">= 0.0.0"}
  end
end
```

Then just call this in your deps list, instead of hard-coding the `:my_library` dependency.

```elixir
defp deps do
  [
    my_library()
  ]
end
```

Finally, we'll check if we're using a relative path in "config/dev.exs" and enable the config changes for live reloading.

```elixir
# Configure Phoenix.CodeReloader to reload my_library as well as this application on every request
config :my_app, MyAppWeb.Endpoint, reloadable_apps: [:my_app, :my_library]

# Configure Phoenix.LiveReloader to watch the CWD and `my_library` paths for file changes
my_library_path = Mix.Project.deps_paths()[:my_library]
config :phoenix_live_reload, :dirs, ["", my_library_path]

# Watch static and templates for browser reloading.
config :my_app, MyAppWeb.Endpoint,
  live_reload: [
    patterns: [
      ~r"priv/static/(?!uploads/).*(js|css|png|jpeg|jpg|gif|svg)$",
      ~r"priv/gettext/.*(po)$",
      ~r"lib/my_app_web/(?:controllers|live|components|router)/?.*\.(ex|heex)$",
      ~r"my_library/lib/.*(ex|heex)$"
    ]
  ]
```

#### Use an optional file to determine the dependency

There are some that would view "reaching" outside a project's working directory, to somewhere else on the developers filesystem, as a violation.
I'm not going to argue one way or another, but leave it up to you.
The advantage of the previous solution is that it "just works", but it requires checking for a directory next to the "my_app/" checkout.
Instead, we could require the user to specifically set the path for the dependency by putting the path in a ".my_library_path" file in the root of "my_app/".
If they don't we fall back to loading the dependency from hex.pm.

Same as the above example, but instead define `my_library/0` as this function, which reads the path from the expected file, and uses it to set the relative dependency. 

```elixir
defp my_library() do
  path_file = Path.expand("./.my_library_path", __DIR__)

  if File.exists?(path_file) do
    path = path_file |> File.read!() |> String.trim()
    {:my_library, path: Path.expand(path, __DIR__)}
  else
    {:my_library, ">= 0.0.0"}
  end
end
```

And then `echo "../my_library" > .my_library_path` or similar to configure it to use the local sibling directory.

Finally configure "config/dev.exs" exactly the same as above.

## Option 2: A subdir Phoenix project

In this scenario, we'll have one parent directory named "my_library/" which will be our package we intend to publish.
Then to test it, we'll create a new Phoenix project in a subdirectory, so that it will be "my_library/my_app/".

Pros:

- Your reference Phoenix application that you develop your library with is in the same git repository.
- Synchronizing changes between the two projects is simple since you commit changes to the same monorepo.
- You can edit everything in one IDE. (See fix below for code formatting.)

Cons:

- Your package repository will be larger, with files and commits for both your library and phoenix app.
- Having two elixir projects open in the same IDE might cause some confusion or issues, depending on your IDE.
- You can't clone just the phoenix project like in Option 1, you have to clone everything (barring some advanced git techniques.)

### Create the library `MyLibrary`

1. Create a new mix project with `mix new my_library`.
1. Change to the new dir with `cd my_library`.
1. Add `:phoenix_live_view` as a dependency to "mix.exs" so we can use `Phoenix.Component`.
   We'll use the spec `~> 1.0` to say our library works with any version of LiveView that is `>= 1.0.0 and < 2.0.0`.
```elixir
defp deps do
  [
    {:phoenix_live_view, "~> 1.0"}
  ]
end
```
1. Run `mix deps.get`
1. Edit "lib/my_library.ex" to be:
```elixir
defmodule MyLibrary do
  use Phoenix.Component

  def hello(assigns) do
    ~H"""
    <div>
      Hello, <%= @name %>!
    </div>
    """
  end
end
```
1. Edit "mix.exs" to add required hex package info in the main `project/0` function:
```elixir
def project do
  [
    app: :my_library,
+   description: "A library of Phoenix LiveView components",
    version: "0.1.0",
    elixir: "~> 1.18",
    start_permanent: Mix.env() == :prod,
    deps: deps(),
+   package: [
+     licenses: ["MIT"],
+     links: %{"GitHub" => "https://github.com/myuser/my_library"}
+   ]
  ]
end
```
1. Run `mix hex.build` to make sure that it will build a package tarball without error.

### Create the phoenix app `MyApp` / `MyAppWeb`

1. While still in "my_library/", create a new Phoenix project with `mix phx.new my_app`.
   Customize with whatever switches you want (e.g. `--no-ecto`, `--no-mailer`, etc).
   Say yes to "Fetch and install dependencies?".
1. Change to the new dir with `cd my_app`.
1. Add the library to the list of deps in "mix.exs" as a relative path.
  This will tell mix to use our library one directory up instead of trying to fetch it from hex.pm.
```elixir
defp deps do
  [
    {:my_library, path: "../"}
  ]
end
```
1. We'll create a new controller just to test with. In "lib/my_app_web/controllers/page_controller.ex" create a new function:
```elixir
def hello(conn, %{"name" => name}) do
  render(conn, "hello.html", name: name)
end
```
1. Create the template "lib/my_app_web/controllers/page_html/hello.html.heex" to go along with this, which is where we're going to call our new `hello` component from `MyLibrary`:
    - **Phoenix < 1.8**
      ```elixir
      <MyLibrary.hello name={@name} />
      ```
    - **Phoenix >= 1.8**
      ```elixir
      <MyAppWeb.Layouts.app flash={@flash}>
        <MyLibrary.hello name={@name} />
      </MyAppWeb.Layouts.app>
      ```
1. Add this new action to your router, right below the one for `:home`:
```elixir
get "/hello/:name", PageController, :hello
```
1. Start up Phoenix with `mix phx.server` (or `iex -S mix phx.server` if you prefer.)
1. Navigate to [http://localhost:4000/hello/mary](http://localhost:4000/hello/mary).
   You should see "Hello, mary!".

!!! accent "Fixing Code Formatting"

    You might be getting a warning from `mix format` or your LSP that the files you modify in "my_library/my_app/" are not included in "my_library/.formatter.exs".
    You can fix that by adding this to "my_library/.formatter.exs":

    ```elixir
    [
      inputs: ["{mix,.formatter}.exs", "{config,lib,test}/**/*.{ex,exs}"],
    + subdirectories: ["my_app"]
    ]
    ```
    
    You might also then get a message about "Unknown dependency :ecto_sql given to :import_deps".
    This is because "my_library/my_app/.formatter.exs" is trying to load formatting options from a dependency it has, but Elixir LS is looking for those dependencies in "my_library/mix.exs".
    The only fix I know for this is to just add that as a dependency in "my_library/mix.exs", but mark it as `only: [:dev, :test]` so that it isn't a dependency of your library (unless that actually is the case!)
    You have to include it in `:test` since that's the environment that ElixirLS compiles in, and `:dev` for running `mix format` on the command line from "my_library/".
    
    ```elixir
    defp deps do
      [
        {:ecto_sql, "~> 3.0", only: [:dev, :test]}
      ]
    end
    ```
    
    Then run `mix deps.get` followed by `mix deps.compile` in "my_library/". You may also need to restart your IDE, or even quit your IDE, delete ".elixir_ls" and restart.
    But hopefully then formatting will work.

### Configuring Phoenix for Live Reloading

At this point you should have a working page that uses the function component from your library.
However, make any kind of change to the function component in "my_library/lib/my_library.ex" and you'll notice a couple problems.

1. The browser doesn't reload on its own when you make a change.
2. Even hitting reload doesn't cause the change to show up.
3. Only stopping and starting the server will make the change appear in the browser.

So first let's get `Phoenix.CodeReloader` working so that `MyLibrary` is recompiled when it changes and the server gets a request.
This is as easy as adding this to our "my_library/my_app/config/dev.exs".

```elixir
# Configure Phoenix.CodeReloader to reload my_library as well as this application on every request
config :my_app, MyAppWeb.Endpoint, reloadable_apps: [:my_app, :my_library]
```

Restart your Phoenix server, make another change to "my_library/lib/my_library.ex", then refresh your browser and you should see the change appear, and a line about compiling "my_library" in your console.

Now that's done, let's get the browser to do the refreshing automatically, by configuring `Phoenix.LiveReloader`.
Again, in "config/dev.exs" add this line:

```elixir
# Configure Phoenix.LiveReloader to watch the CWD and `my_library` paths for file changes
config :phoenix_live_reload, :dirs, ["", "../"]
```

This will cause `Phoenix.LiveReloader` to now watch our parent directory in addition to the phoenix "my_app" directory.
However, it will most likely be filtering out these notifications, so we'll need to also add a line to the patterns so that it includes these changes as valid.

```elixir
# Watch static and templates for browser reloading.
config :my_app, MyAppWeb.Endpoint,
  live_reload: [
    patterns: [
      ~r"priv/static/(?!uploads/).*(js|css|png|jpeg|jpg|gif|svg)$",
      ~r"priv/gettext/.*(po)$",
      ~r"lib/my_app_web/(?:controllers|live|components|router)/?.*\.(ex|heex)$",
+     ~r"lib/my_library.*(ex|heex)$"
    ]
  ]
```

Restart your Phoenix server one last time, again make a change to "my_library/lib/my_library.ex", and as soon as you save you should see the browser refresh and the change appear on its own.
If you don't, then recheck these steps and also review the sections above on [`Phoenix.CodeReloader`](#the-code-reloader) and [`Phoenix.LiveReloader`](#the-live-reloader)

## Option 3: Umbrella

In this scenario, we'll create a new Phoenix project as an Umbrella, then create our library as one of the "apps" under it, in the "apps/" directory.
When publishing our library, we will publish from "apps/my_library" instead of the root of the project, like the other options.

!!! warning "This is not recommended"
    I have to say that I do not recommend this option.
    Umbrellas just make things extra complex for little to no gain.
    I would suggest using one of the other options first, and only use this option if you really think you want to, or already have an umbrella project.
    This is really just here because it's possible and I feel remiss not mentioning it.

Pros:

- You have one monorepo with many possibly unrelated apps in it, including your package.
- Synchronizing changes between the projects is simple since you commit both to the same monorepo.
- You can edit everything in one IDE.

Cons:

- Umbrellas make things much more complicated.
- Your library is buried inside what looks like a Phoenix Umbrella project, making it difficult for people to understand.
- Your docs published to hexdocs will need to have [extra work done](https://elixirforum.com/t/hex-package-from-umbrella-subapp/48034/2) to make source links work properly.
- Running your library through CI/CD [will be more complicated.](https://elixirforum.com/t/hex-package-from-umbrella-subapp/48034/2)
- Your package repository will be larger, with files and commits for both your library and phoenix app.
- Your IDE might not support umbrella projects properly.
- You can't clone just the phoenix project like in Option 1, you have to clone everything (barring some advanced git techniques.)

### Create the phoenix umbrella

1. Create a new Phoenix umbrella project with `mix phx.new my_app --umbrella`.
   Customize with whatever switches you want (e.g. `--no-ecto`, `--no-mailer`, etc.)
   Say yes to "Fetch and install dependencies?".
1. Change to the new dir with `cd my_app_umbrella`.

### Create the library `MyLibrary`

1. Change to the apps dir with `cd apps`. 
1. Create a new mix project with `mix new my_library`. Mix will detect that this is inside of an umbrella and configure the library accordingly.
1. Change to the new dir with `cd my_library`.
1. Add `:phoenix_live_view` as a dependency to "apps/my_library/mix.exs" so we can use `Phoenix.Component`.
   We'll use the spec `~> 1.0` to say our library works with any version of LiveView that is `>= 1.0.0 and < 2.0.0`.
```elixir
defp deps do
  [
    {:phoenix_live_view, "~> 1.0"}
  ]
end
```
1. Run `mix deps.get` from the parent directory of the umbrella.
1. Edit "apps/my_library/lib/my_library.ex" to be:
```elixir
defmodule MyLibrary do
  use Phoenix.Component

  def hello(assigns) do
    ~H"""
    <div>
      Hello, <%= @name %>!
    </div>
    """
  end
end
```
1. Edit "mix.exs" to add required hex package info in the main `project/0` function:
```elixir
def project do
  [
    app: :my_library,
+   description: "A library of Phoenix LiveView components",
    version: "0.1.0",
    build_path: "../../_build",
    config_path: "../../config/config.exs",
    deps_path: "../../deps",
    lockfile: "../../mix.lock",
    elixir: "~> 1.18",
    start_permanent: Mix.env() == :prod,
    deps: deps(),
+   package: [
+     licenses: ["MIT"],
+     links: %{"GitHub" => "https://github.com/myuser/my_library"}
+   ]
  ]
end
```
1. Run `mix hex.build` in "apps/my_library/" to make sure that it will build a package tarball without error.

### Configure the "MyAppWeb" umbrella app

1. Add the library to the list of deps in "apps/my_app_web/mix.exs" as an umbrella path.
   This tells mix that the dependency is another app in the same umbrella. 
```elixir
defp deps do
  [
    {:my_library, in_umbrella: true}
  ]
end
```
1. We'll create a new controller just to test with. In "apps/my_app_web/lib/my_app_web/controllers/page_controller.ex" create a new function:
```elixir
def hello(conn, %{"name" => name}) do
  render(conn, "hello.html", name: name)
end
```
1. Create the template "apps/my_app_web/lib/my_app_web/controllers/page_html/hello.html.heex" to go along with this, which is where we're going to call our new `hello` component from `MyLibrary`:
    - **Phoenix < 1.8**
      ```elixir
      <MyLibrary.hello name={@name} />
      ```
    - **Phoenix >= 1.8**
      ```elixir
      <MyAppWeb.Layouts.app flash={@flash}>
        <MyLibrary.hello name={@name} />
      </MyAppWeb.Layouts.app>
      ```
1. Add this new action to your router, right below the one for `:home`:
```elixir
get "/hello/:name", PageController, :hello
```
1. Change back to the root directory of the umbrella, that has the "apps/" subdir.
1. Start up Phoenix with `mix phx.server` (or `iex -S mix phx.server` if you prefer.)
1. Navigate to [http://localhost:4000/hello/arnold](http://localhost:4000/hello/arnold).
   You should see "Hello, arnold!".

### Configuring Phoenix for Live Reloading

At this point you should have a working page that uses the function component from your library.
You should even be able to make a change to "apps/my_library/lib/my_library.ex", refresh the page, and see the changes.
This is because `Phoenix.CodeReloader` detects that it's running in an umbrella app, and by default will recompile all apps every time it gets a request.
This is the only real advantage of umbrellas (but still not worth it, imo.)
However, you still have to refresh the page to see the pages, so let's get `Phoenix.LiveReloader` working as well so it auto-refreshes.

In "config/dev.exs" add these lines, per [the example in the docs](https://hexdocs.pm/phoenix_live_reload/Phoenix.LiveReloader.html#module-configuration).

```elixir
root_path = __ENV__.file |> Path.dirname() |> Path.join("..") |> Path.expand()

# Configure Phoenix.LiveReloader to watch the `my_app_web` and `my_library` paths for file changes
config :phoenix_live_reload, :dirs, [
 Path.join([root_path, "apps", "my_library"]),
 Path.join([root_path, "apps", "my_app_web"])
]
```

This will cause `Phoenix.LiveReloader` to now watch both of those apps directories for changes.
However, it will most likely be filtering out these notifications, so we'll need to also add a line to the patterns so that it includes these changes as valid.

```elixir
# Watch static and templates for browser reloading.
config :my_app, MyAppWeb.Endpoint,
  live_reload: [
    patterns: [
      ~r"priv/static/(?!uploads/).*(js|css|png|jpeg|jpg|gif|svg)$",
      ~r"priv/gettext/.*(po)$",
      ~r"lib/my_app_web/(?:controllers|live|components|router)/?.*\.(ex|heex)$",
+     ~r"lib/my_library.*(ex|heex)$"
    ]
  ]
```

Restart your Phoenix server, make a change to "apps/my_library/lib/my_library.ex", and as soon as you save you should see the browser refresh and the change appear on its own.
If you don't, then recheck these steps and also review the sections above on [`Phoenix.CodeReloader`](#the-code-reloader) and [`Phoenix.LiveReloader`](#the-live-reloader)

# Publishing your package

Now that you have a working dev environment set up, with live reloads, it's time to get cracking on your package!
Remember to tweak the `patterns` if you need to, based on what files you want to cause live reloads when they change.
This will depend on your package and what it does!

Once you're ready, [follow the publishing guide](https://hex.pm/docs/publish) to set any other options you want, build your docs, etc.
With all 3 options you should be able to cd into your "my_library/" directory and `mix hex.publish`.

For Option 3, the umbrella, you might have some extra work. I have never done it myself, but you can refer to [this post](https://elixirforum.com/t/hex-package-from-umbrella-subapp/48034/2) on the Elixir Forums for help, and the linked example [monorepo](https://github.com/straw-hat-team/beam-monorepo) for a few published hex packages for guidance.

If you find an issue with this guide, please hit the "Contact Me" link in the footer.

Happy packaging!

*[DX]: Developer eXperience
*[CWD]: Current Working Directory
*[IDE]: Integrated Development Environment (code editor)
*[CI]: Continuous Integration
*[CD]: Continuous Delivery
