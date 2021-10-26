Title: Fixing Lua indenting in Sublime Text
Date: 2013-04-10
Status: published
URL: 2013/04/fixing-lua-indenting-in-sublime-text.html
Save_as: 2013/04/fixing-lua-indenting-in-sublime-text.html
Summary: I recently started using Sublime Text 2 to edit the Lua project I'm working on, however, it did a couple strange things with indenting. Here is how I fixed them.
Modified: 2015-09-18
Tags: lua, sublime-text

*Updated September 18th, 2015: Added info on making the same changes to latest ST2 and ST3 build 3083*

I recently started using Sublime Text to edit the Lua project I'm working on, however, it did a couple strange things with indenting. Here is how I fixed them.

First, open the file we need to edit in your Sublime Packages Lua directory.

#### Sublime Text 2:

* Find your Packages directory by going to **Preferences** -> **Browse Packages...** in Sublime Text.
* Open the **Lua** folder
* Edit the **Indent.tmPreferences** file

#### Sublime Text 3:

* Install PackageResourceViewer using Package Control or from https://github.com/skuroda/PackageResourceViewer
* Run **PackageResourceViewer: Open Resource**
* Select *Lua* then *Indent.tmPreferences*

In that file you'll see keys labeled, `increaseIndentPattern` and `decreaseIndentPattern` with accompanying regexes wrapped in `<string>` entities. We'll be editing those for these two fixes.

### Nested curly brace indentation

First, whenever you nested curly braces, indenting any curly braces after the first one would end up with something like this:

![Invalid tabbing for nested curly braces]({static}/images/fixing-sublime-lua/sublime_curly_bad.png)

When instead we want something like this:

![Valid tabbing for nested curly braces]({static}/images/fixing-sublime-lua/sublime_curly_good.png)

The fix for this is pretty easy. We want to edit the `increaseIndentPattern`

```xml
<key>increaseIndentPattern</key>
<string>^\s*(else|elseif|for|(local\s+)?function|if|repeat|until|while)\b((?!end).)*$|.*\{\s*$</string>
```

The first half is concerned with matching keywords like "if" and "for", but without also having "end" on the same line. The latter half is the part we care about.

```perl
|\{\s*$
```

This matches a curly brace followed by zero or more whitespace characters then the EOL. At first glance this seems like it would work. The fix, weirdly enough, is to match anything before the curly brace as well. So we add ".*" which matches any character zero or more times. I think it might be because sublime throws out any partial matches to prevent erroneous indents. It wants the whole line to be matched. So the fix looks like:

```perl
|.*\{\s*$
```

This does mean that it will indent ANY line ending in a curly brace.

### Strange indentation of "elseif"

The other problem is improper indentation of the "elseif" statement. Basically sublime gets really confused because it matches "else" then "elseif" and then "elseif" with something after it, and it ends up not recognizing the statement as valid, and doesn't know to unindent it. It looks like this bit of strangeness:

![Bad elsif indentation]({static}/images/fixing-sublime-lua/sublime_elseif_bad.gif)

The problem here lies in the "decreaseIndentPattern" part.

```xml
<key>decreaseIndentPattern</key>
<string>^\s*(elseif|else|end|\})\s*$</string>
```

This works fine for "else" and "end" because the don't have anything after them. However, "elseif" by it's nature will have text coming after it. So to fix this, we are going to remove "elseif" from this statement, and break it out into its own sub-regex. That way "else" and "end" will continue to work like they should. Then we're going to tell it that "elseif" can have characters after it, but only if there is no "end" after the "elseif". You might have noticed that this sounds like what it does in the "increaseIndentPattern" part. So we can just copy that bit of regex to fit this need as well. We end up with:

```xml
<string>^\s*(else|end|\})\s*$|^\s*elseif\b((?!end).)*$</string>
```

After the "|" we put in, it matches zero or more whitespace, the word "elseif" followed by a word boundary, then it does a look-ahead to match any character that doesn't follow "end" zero or more times before finding the end-of-line. This results in proper behavior:

![Good elsif indentation]({static}/images/fixing-sublime-lua/sublime_elseif_good.gif)

### Fully fixed file

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>name</key>
	<string>Indent</string>
	<key>scope</key>
	<string>source.lua</string>
	<key>settings</key>
	<dict>
		<key>decreaseIndentPattern</key>
		<string>^\s*(else|end|\})\s*$|^\s*elseif\b((?!end).)*$</string>
		<key>increaseIndentPattern</key>
		<string>^\s*(else|elseif|for|(local\s+)?function|if|repeat|until|while)\b((?!end).)*$|.*\{\s*$</string>
	</dict>
	<key>uuid</key>
	<string>411468A8-E0AC-415A-9E71-E2BD091EB571</string>
</dict>
</plist>
```

### Restart Sublime Text

#### Sublime Text 2:

Just restart and your changes should take effect.

#### Sublime Text 3:

* Find your Packages directory by going to "Preferences->Browse Packages..." in Sublime Text 3.  Leave this window open.
* Close all Sublime Text 3 windows
* Back in your file browser window, navigate up one directory then delete the "Cache" directory.
* Start Sublime Text 3 and it should work now.

