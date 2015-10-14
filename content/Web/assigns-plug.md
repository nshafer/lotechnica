Title: A Phoenix Plug for assigning template variables
Date: 2015-10-05
Modified: 2015-10-14
Status: published
Small_image: images/phoenix/plug_small.jpg
Jumbo_image: images/phoenix/plug.jpg
Jumbo_attr: Todd Ehlers
Jumbo_attr_link: https://www.flickr.com/photos/eklektikos/371357839
Jumbo_color: dark
Tags: phoenix, elixir, plug

Here's a quick [Plug](http://www.phoenixframework.org/v0.11.0/docs/understanding-plug) for a [Phoenix](http://www.phoenixframework.org/) project that allows you to quickly and easily set template variables (assigns) in either a [Pipeline](http://www.phoenixframework.org/docs/routing) or for all actions in a controller. I used this recently as a way to set a variable, `admin: true`, for all of my controllers under an `/admin` scope.  I also used it to set a `subsection` variable for the different controllers that make up the different parts of the site so that my Layout template could mark which section of the site the user was currently on in the site navigation header.

>***Update 10/14/15**: I went ahead and published this as a self-contained hex package, if nothing else than as an exercise in publishing things.  It's [available on hex.pm](https://hex.pm/packages/plug_assign/1.0.0).  Note that I renamed it to `Plug.Assign` to better match existing Plug names.*

### The Plug

The Plug itself is very straightforward since we're able to exploit the fact that Phoenix just uses Plug's [`assigns`](http://hexdocs.pm/plug/Plug.Conn.html#t:assigns/0) map that is part of the [`Plug.Conn`](http://hexdocs.pm/plug/Plug.Conn.html) struct as the holding place for template context variables.  Thus we can assign our own variables as part of the Plug stack before the Controller action (which itself is just a plug) even executes.  So our first step is going to be creating the plug.

As an interface, our plug will accept a map of key/value pairs, exactly like the [`render/3`](http://hexdocs.pm/phoenix/Phoenix.Controller.html#render/3) function in a Controller/View.  So as an example, it will look like:

```elixir
plug Plugs.Assigns, foo: "This is foo", bar: true, baz: 5
```

I decided to put it in `lib/plugs` and named the source file `assigns.ex` so that my module name will be `Plugs.Assigns`.  This way I can easily copy this plug to other projects.  It could even be packaged up as a Hex package and installed as a dependency.  So `lib/plugs/assigns.ex` will look like:

```elixir
defmodule Plugs.Assigns do
	import Plug.Conn

	def init(assigns), do: assigns

	def call(conn, assigns) do
		Enum.reduce assigns, conn, fn {k, v}, conn ->
			Plug.Conn.assign(conn, k, v)
		end
	end
end
```

If you're not familiar with the [Plug spec](http://hexdocs.pm/plug/Plug.html), two functions are required, `init/1` and `call/2`.  We don't need to do anything with the map at initialization time, so our `init/1` function just returns it.  However, for each request, our `call/2` function will take the `assigns` map and add it to the `conn`.  This could possibly be written more efficiently by directly manipulating the `assigns` map in the `Plug.Conn` struct `conn`, but I opted to use the interface so that it uses the public [`Plug.Conn.assign`](http://hexdocs.pm/plug/Plug.Conn.html#assign/3) function, making it more compatible with possible future changes to Plug.

### Using in a Pipeline

Let's say you want to assign a variable `admin` to either `true` if the current request is being routed to an `/admin` scope.  For example, you have something like this defined in your `routers.ex`:

```elixir
defmodule Blog.Router do
  use Blog.Web, :router

  pipeline :browser do
    plug :accepts, ["html"]
    plug :fetch_session
    plug :fetch_flash
    plug :protect_from_forgery
    plug :put_secure_browser_headers
  end

  scope "/", Blog do
    pipe_through :browser # Use the default browser stack

    get "/", PageController, :index
    get "/post/:post_id", PageController, :post
  end

  scope "/admin", Blog.Admin do
    pipe_through :browser # Use the default browser stack

    resources "/posts", PostController
    resources "/users", UserController
  end
end
```

Now let's say you would like to modify your `layout/app.html.eex` template so that it has "Admin: " prefixed to the page title, as an example.

```eex
<title><%= if assigns[:admin], do: "Admin: " %>My Blog!</title>
```

We would do this by defining a new pipeline in `router.ex`, and call it `:admin`:

```elixir
pipeline :admin do
  plug Plugs.Assigns, %{admin: true}
end
```

And then we can modify our `/admin` scope to use it.

```elixir
scope "/admin", Blog.Admin do
  pipe_through [:browser, :admin] # Use admin stack as well

  resources "/posts", PostController
  resources "/users", UserController
end
```

Now all requests to any controller under `/admin` will include the variable `admin: true`.

### Using it to assign a variable for all Controllers

Another way to use this would be to set a variable for all action functions in a Controller.  To continue our example, in our `web/controllers/admin/post_controller.ex` file, we could just add a plug call to our custom Plug near the top.

```elixir
defmodule Blog.Admin.PostController do
  use Blog.Web, :controller

  alias Blog.Post

  plug :scrub_params, "post" when action in [:create, :update]
  plug Plugs.Assigns, subsection: :posts

  ...
end
```

Our corresponding template could check if the `subsection` variable is set to something specific to enable a visual indication of what subsection the user is currently in.

```eex
<li class="<%= if assigns[:subsection] == :posts do "active" end %>">
    <a href="<%= post_path(@conn, :index) %>">Posts</a>
</li>
```

If you wanted to limit the plug to only certain actions, this could be done by adding a `when` clause.  However, do note that when you do that, the map of assigns will no longer be the last predicate, and so you need to wrap it in a map operator, `%{}`.

```elixir
plug Plugs.Assigns, %{subsection: :posts} when action in [:index, :show]
```

Now the `subsection` variable will only be set to `:posts` when the user is calling the `:index` and `:show` actions.

So there's an example of how powerful the Plug interface is, and how it allows you to add so much functionality with almost no code.
