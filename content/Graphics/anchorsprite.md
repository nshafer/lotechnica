Title: AnchorSprite: Setting an anchor point on any Sprite
Date: 2013-06-12
Status: published
URL: 2013/06/anchorsprite-setting-anchor-point-on.html
Save_as: 2013/06/anchorsprite-setting-anchor-point-on.html
Summary: A class to allow you to set arbitrary anchor points on any sprite with little overhead.
Tags: lua, gideros

Having done a lot of work with matrices in [Gideros](http://giderosmobile.com/) recently, during a [discussion at the Gideros forums](http://www.giderosmobile.com/forum/discussion/comment/23535#Comment_23535) it occurred to me that with the Matrix class that I [recently covered]({filename}/Graphics/beauty-matrix-transforms.md), I could possibly address an oft-requested feature of Gideros.  The problem is that in Gideros, all Sprite objects have an anchor point of [0,0] that you can't change.  So all transformations such as rotation and scaling are relative to the top left point of the Sprite.  The one exception to this is with Bitmap objects, where there is a `setAnchorPoint()` method.  But this doesn't help for other Sprite based objects, such as TextFields or Shapes.

So I whipped together a class called [AnchorSprite](https://github.com/nshafer/AnchorSprite/blob/master/AnchorSprite.lua), which when added to your project, adds a `setAnchorPoint()` and `getAnchorPoint()` method to every Sprite object and all objects that inherit from Sprite.  Further, [bowerandy](http://www.giderosmobile.com/forum/profile/315/bowerandy) had the [great idea](http://www.giderosmobile.com/forum/discussion/comment/23615#Comment_23615) to make this support completely inactive until you set an anchor, that way you could avoid any overhead on sprites that still had the default anchor point.

So I'm going to explain a little bit about how this class works.  I'm going to skip over most of the matrix stuff since I [already covered that in detail]({filename}/Graphics/beauty-matrix-transforms.md).

### Intercepting Sprite transform methods

The first step is to intercept all calls to transform methods of the `Sprite` class.  This includes `setPosition()`, `setScale()`, `setRotation()` as well as all the other specific ones, `setX()`, `setScaleY()`, etc.  We also need to intercept `set()` itself.  We have to do this, because we don't want the Sprite class to actually change anything.  Instead, we just take the desired changes and save them in private member variables.  For example, here is how we intercept `set()`.

```lua
-- Intercept Sprite's set and get functions for position, scale and rotation
function AnchorSprite:set(key, value)
	if value then
		if key == "x" then
		   self._positionX = value
		elseif key == "y" then
		   self._positionY = value
		elseif key == "scaleX" then
		   self._scaleX = value
		elseif key == "scaleY" then
		   self._scaleY = value
		elseif key == "rotation" then
		   self._rotation = value
		else
		   self._anchorBackup.set(self, key, value)
		end
		self:_applyTransforms()
	end
end
```

You'll notice that this is in the `AnchorSprite` class and not the `Sprite` class just yet.  We don't want to intercept it until an anchor point is set, which I'll show in a bit.

So just to show another example, this is what our intercepted `setPosition()` method will look like.

```lua
function AnchorSprite:setPosition(x, y)
	self:set("x", x)
 	self:set("y", y)
end
```

### Applying the transforms

The thing to notice is that we're not doing anything with the values being passed in, just storing them in private member variables.  This is because we need to basically keep a stack of transforms in memory, so that we can apply them all whenever any of them change.  This is done in the `_applyTransforms`method, which is called every time `set()` is called.

```lua
-- New function to apply all transforms whenever anything changes
function AnchorSprite:_applyTransforms()
```

This function will do all the calculations needed to apply the transforms.  It starts from scratch with a brand new Matrix.

```lua
 	-- Create a new identity matrix
 	local matrix = Matrix.new()
```

We then apply that new matrix to the sprite, thus resetting it back to completely default location, rotation and scale.  This is so we can get an accurate width and height, so we know how to apply the anchor, which is specified as a percentage of the dimensions of the Sprite.  We could forgo this and just have the anchor set as a specific pixel location, but I chose to do it this way to mirror the way that the `Bitmap:setAnchorPoint()` works.  Plus it means you can change the dimensions of the `Sprite` and always know that the anchor point will be in the place you expect without having to calculate the anchor point yourself.

```lua
 -- Zero ourselves out so we can get accurate width and height
 self:setMatrix(matrix)

 -- Calculate the actual position of the anchor
 local anchorOffsetX = self._anchorPointX * self:getWidth()
 local anchorOffsetY = self._anchorPointY * self:getHeight()
```

The next set of operations apply our transformations to the Matrix, effectively concatenating them.  They should all be pretty self explanatory if you've read my [matrix overview]({filename}/Graphics/beauty-matrix-transforms.md).  In short, each is in turn concatenated onto the matrix much like characters can be concatenated together to form a string.  First we set the position, then rotation and scale.

```lua
 -- set position
 matrix:translate(self._positionX, self._positionY)
 
 -- concatenate rotation and scale matrices
 matrix:rotate(self._rotation)
 matrix:scaleX(self._scaleX)
 matrix:scaleY(self._scaleY)
```

And finally the magic part, which is to offset by the negative of the anchor point.

```lua
 -- concatenate offset to new origin in modified coordinate space
 matrix:translate(-anchorOffsetX, -anchorOffsetY)
```

Since we concatenate the anchor point translate last, it is applied to the new coordinate space that is a result of the previous concatenations, and not based on the original coordinate space.  Thus if you have an anchor point of [.5,.5] and rotate clockwise 45 degrees, the last translate will move the whole sprite along that 45 degree angle, or basically straight up.  If you were to try this with the original Sprite:setPosition, it would move based on the original coordinate space, and so end up moving the sprite up and to the left, which is not what you wanted.

Lastly we apply our built-up matrix with `setMatrix()`, thus causing all the transforms to get applied.  This will affect the current sprite as well as any children in the scene graph.

```lua
 -- Apply the new matrix
 self:setMatrix(matrix)
```

This is our finished `_applyTransforms()` function.

```lua
-- New function to apply all transforms whenever anything changes
function AnchorSprite:_applyTransforms()
 	-- Create a new identity matrix
 	local matrix = Matrix.new()
 	
 	-- Zero ourselves out so we can get accurate width and height
 	self:setMatrix(matrix)
	
 	-- Calculate the actual position of the anchor
 	local anchorOffsetX = self._anchorPointX * self:getWidth()
 	local anchorOffsetY = self._anchorPointY * self:getHeight()
 	
 	-- set position
 	matrix:translate(self._positionX, self._positionY)
 	
 	-- concatenate rotation and scale matrices
 	matrix:rotate(self._rotation)
 	matrix:scaleX(self._scaleX)
 	matrix:scaleY(self._scaleY)
 	
 	-- concatenate offset to new origin in modified coordinate space
 	matrix:translate(-anchorOffsetX, -anchorOffsetY)
 	
 	-- Apply the new matrix
 	self:setMatrix(matrix)
end
```

### Optimization

So the last bit is to make this code only get put into place when an anchor point is set.  This way, after you add `AnchorPoint.lua` to your project, it doesn't do anything to any `Sprite`s by default.  Only those that you set an anchor point for with `setAnchorPoint` will start to intercept the transform methods, thus resulting in less overhead.  This is why our functions so far have been in the `AnchorSprite` class.  First step is to add the `setAnchorPoint()` method to the `Sprite` class along with our private member variables for storing the transforms.

```lua
Sprite._anchorSupport = false
Sprite._anchorBackup = {}
Sprite._anchorPointX = 0
Sprite._anchorPointY = 0
Sprite._positionX = 0
Sprite._positionY = 0
Sprite._scaleX = 1
Sprite._scaleY = 1
Sprite._rotation = 0

-- New functions in Sprite for setting the anchor
function Sprite:setAnchorPoint(x, y)
 	self._anchorPointX = x
 	self._anchorPointY = y or x
 
 	if x ~= 0 or y ~= 0 and not self._anchorSupport then
  	self:_enableAnchorSupport()
 	elseif x == 0 and y == 0 and self._anchorSupport then
  	self:_disableAnchorSupport()
 	end
end
```

As you can see, this mainly calls a function called `_enableAnchorSupport()` that does all the work of modifying the Sprite class accordingly.

```lua
function Sprite:_enableAnchorSupport()
 	self._anchorSupport = true
 	
 	-- Get current values
 	self._positionX = self:getX()
 	self._positionY = self:getY()
 	self._scaleX = self:getScaleX()
 	self._scaleY = self:getScaleY()
 	self._rotation = self:getRotation()
 	
 	-- Override Sprite functions with AnchorSprite versions
 	for k,v in pairs(AnchorSprite) do
 	 	if type(v) == "function" then
 	 	 	--print("AnchorSprite", k, v)
 	 	 	if self[k] then
 	 	 	 	-- Backup existing function
 	 	 	 	self._anchorBackup[k] = Sprite[k]
 	 	 	end
 	 	 	
 	 	 	-- Replace with AnchorSprite version
 	 	 	self[k] = v
 	 	end
 	end
 	
 	self:_applyTransforms()
end
```

This initializes our transform variables, then does a bit of magic of modifying the `Sprite` class itself.  If you're unfamiliar with how Lua works, the thing to remember is that almost everything in Lua is a table.  All classes are just a table, and values of that table can be variables or references to functions.  So after backing up the original reference in `_anchorBackup` (a table), we just replace the reference in `Sprite`'s table with the one in `AnchorSprites` table.  So now functions like `AnchorSprite:_applyTransforms` from earlier are now `Sprite:_applyTransforms`.  The methods in `AnchorSprite` are never meant to be called while they're in `AnchorSprite`, and would actually throw weird errors.  We make backups so that if the anchor is reset to [0,0], we can called `_disableAnchorSupport()` and return `Sprite` to the way it was.

### Result

<iframe style="float: right; margin-left: 25px;" width="420" height="315" src="http://www.youtube.com/embed/mM4SZwYuWOM?rel=0" frameborder="0" allowfullscreen></iframe>

In the end, the result is that to the user, all we've done is added `Sprite:setAnchorPoint()` and `Sprite:getAnchorPoint()`, and everything just works.  A [sample project is available](https://github.com/nshafer/AnchorSprite) to see how it can be implemented and to show the results.  To use it, simply include [AnchorSprite.lua](https://github.com/nshafer/AnchorSprite/blob/master/AnchorSprite.lua) and [Matrix.lua](https://github.com/nshafer/AnchorSprite/blob/master/Matrix.lua) into your project.

Of course, this is hopefully just a stopgap solution until Gideros builds this functionality in.  Until then, this is one way to get around the limitation.  Let me know if you find it useful.
