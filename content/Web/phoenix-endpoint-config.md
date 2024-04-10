Title: Dynamic configuration for Phoenix Endpoints
Date: 2024-04-02
Modified: 2024-04-10
Status: published
Tags: phoenix, elixir

>***Update 2024-04-10**: This article has been updated with a better Workaround that uses your generated MyappWeb.Endpoint.start_link/1. The original article called directly into Phoenix.Endpoint.Supervisor which was more brittle.*

In Phoenix 1.7.11, the `Endpoint.init/2` callback was deprecated. If you have defined it, then you will get this warning on startup:

```elixir
warning: MyappWeb.Endpoint.init/2 is deprecated, use config/runtime.exs instead or pass
         additional options when starting the endpoint in your supervision tree
  (phoenix 1.7.11) lib/phoenix/endpoint/supervisor.ex:36: Phoenix.Endpoint.Supervisor.init/1
  (stdlib 5.2) supervisor.erl:330: :supervisor.init/1
  (stdlib 5.2) gen_server.erl:980: :gen_server.init_it/2
  (stdlib 5.2) gen_server.erl:935: :gen_server.init_it/6
  (stdlib 5.2) proc_lib.erl:241: :proc_lib.init_p_do_apply/3
```

The suggestions given may work fine for you. However, if you're relying on some other part of the system's supervisor tree to be up and running for the config, then those solutions will not work. The reason is that both happen before the main application supervision tree is started by the main Supervisor. The "config/runtime.exs" file is evaluated as the VM is starting up. And if you try to configure the Endpoint via the list of child_specs for the Supervisor in "lib/myapp/application.ex" then that config will be evaluated before the Supervisor starts any of the children.

## Example

An example of this is if you rely on your Ecto Repo to be available to help configure how the Endpoint will run. For example, before 1.7.11 you could have the following in your "lib/myapp_web/endpoint.ex" file:

```elixir
# Note: this is very simplified to illustrate the inability to use Myapp.Repo at this time.

def init(:supervisor, config) do
  # Get the hostname as configured by the user and stored in the database
  hostname = Myapp.Repo.get_by!(TenantSetting, key: "hostname")
  
  # Configure the Endpoint to use the hostname in generated URLs
  {:ok, Keyword.put(config, :url, scheme: "http", host: hostname, port: 4000)}
end
```

You could try to duplicate this functionality by passing options when starting the Endpoint in the main application supervision tree, as suggested, such as:

```elixir
defmodule Myapp.Application do
  use Application

  def start(_type, _args) do
    children = [
      Myapp.Repo,
      ...
      
      # Attempt to dynamically configure the endpoint using the 2-tuple argument
      {MyappWeb.Endpoint, endpoint_config()}
    ]

    opts = [strategy: :one_for_one, name: Myapp.Supervisor]
    Supervisor.start_link(children, opts)
  end
  
  defp endpoint_config() do
    # Try to fetch dynamic run-time configuration from the DB. This will fail!
    hostname = Myapp.Repo.get_by!(TenantSetting, key: "hostname")
    
    [url: [scheme: "http", host: hostname, port: 4000]]
  end
end
```

However, since this runs before `Myapp.Repo` is started, it will fail with the error "(RuntimeError) could not lookup Ecto repo Myapp.Repo because it was not started or it does not exist".

## Workaround

If this callback stays deprecated, this is a way to configure the endpoint dynamically before it starts up, but after the rest of the supervision tree has been started, such as after the Ecto Repo is running and available. It works by intercepting the `start_link/1` call from the main Supervisor, then starting the Endpoint.Supervisor directly with options derived at that point in time.

First, create a new module: "/lib/myapp_web/endpoint/config.ex" with these contents, but with all occurances of `MyappWeb` replaced with your actual module name.

```elixir
defmodule MyappWeb.Endpoint.Config do
  @moduledoc """
  This will start up the MyappWeb.Endpoint as normal, but only after injecting some custom
  configuration that is retrieved from the database after the rest of the application stack
  has started. This needs to be placed in the list of Application children after
  MyappWeb.Repo and any other dependent children to work correctly.

  Prior to Phoenix 1.7.11, this configuration was done in the `init/1` callback of
  MyappWeb.Endpoint. But that callback is now deprecated. The deprecation suggests to
  "use config/runtime.exs instead or pass additional options when starting the endpoint in
  your supervision tree" but the problem with both of these suggestions is that they happen
  before the rest of the supervision tree is started. "runtime.exs" is evaluated during
  vm boot, and the list of children and their options is evaluated as soon as the
  supervisor starts, but before children are started.
  
  So this mimics the original behavior by intercepting the `start_link/1` call from the
  Supervisor to fetch the configuration options at that point. This will happen after the
  previous children in the main Supervision tree are already started.
  """

  def child_spec(opts) do
    %{
      id: MyappWeb.Endpoint,
      start: {MyappWeb.Endpoint.Config, :start_link, [opts]},
      type: :supervisor
    }
  end

  def start_link(opts) do
    dynamic_config(opts)
    |> MyappWeb.Endpoint.start_link()
  end

  defp dynamic_config(opts) do
    hostname = Myapp.Repo.get_by!(TenantSetting, key: "hostname")
    Keyword.put(opts, :url, scheme: "http", host: hostname, port: 4000)
  end
end
```

Then change your main supervision tree in "lib/myapp/application.ex" to include this module in the list of children instead of the original Endpoint module:

```elixir
defmodule Myapp.Application do
  use Application

  def start(_type, _args) do
    children = [
      Myapp.Repo,
      ...
      # Replace "MyappWeb.Endpoint" with:
      MyappWeb.Endpoint.Config
    ]

    opts = [strategy: :one_for_one, name: Myapp.Supervisor]
    Supervisor.start_link(children, opts)
  end
end
```

### Caveats

This makes some assumptions about how the `use Phoenix.Enpoint` macro injects child_spec/1 and start_link/1 into your MyappWeb.Endpoint file. If this is ever changed, this Config module will also need to be updated. However, since these are standard callbacks dictate by Supervisor, it's unlikely that this will happen.

## Fix?

I have submitted an [issue](https://github.com/phoenixframework/phoenix/issues/5771) to the phoenix github repository requesting this deprecation be rolled back.
