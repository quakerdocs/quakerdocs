Customize your documentation with Quaker Docs
=============================================

QuakerDocs supports customizing your own documentation build with a
configuration file. This file is named `conf.py` and is found in the
/docs directory.

Provided stylesheets
--------------------

We provide you with the following 6 stylesheets which are bulma.io
compatible. Thanks to <https://jenil.github.io/bulmaswatch/> for the
provided stylesheets.

### Bulma.min

``` {code-block} python
html_style = 'css/bulma.min.css'
```

|bulma-min-png|

### Bulma.min-classy

``` {code-block} python
html_style = 'css/bulma.min-classy.css'
```

|bulma-min-classy-png|

### Bulma.min-dark

``` {code-block} python
html_style = 'css/bulma.min-dark.css'
```

|bulma-min-dark-png|

### Bulma.min-jet

``` {code-block} python
html_style = 'css/bulma.min-jet.css'
```

|bulma-min-jet-png|

### Bulma.min-night

``` {code-block} python
html_style = 'css/bulma.min-night.css'
```

|bulma-min-night-png|

### Bulma.min-red

``` {code-block} python
html_style = 'css/bulma.min-red.css'
```

|bulma-min-red-png|

Adding your own css
-------------------

You can always add more stylesheets to the already provided stylesheets
by visiting [Bulmaswatch](https://jenil.github.io/bulmaswatch/) . Just
download the style and give a shoutout to bulma afterwards on
[Twitter](https://twitter.com/) .

Add the css file to `static/css` and change the html\_style to the given
name.
