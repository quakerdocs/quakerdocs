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

![Bulma Default](_static/_images/bulma.min.png)

### Bulma.min-classy

``` {code-block} python
html_style = 'css/bulma.min-classy.css'
```

![Bulma Classy](_static/_images/bulma.min-classy.png)

### Bulma.min-dark

``` {code-block} python
html_style = 'css/bulma.min-dark.css'
```

![Bulma Dark](_static/_images/bulma.min-dark.png)

### Bulma.min-jet

``` {code-block} python
html_style = 'css/bulma.min-jet.css'
```

![Bulma Jet](_static/_images/bulma.min-jet.png)

### Bulma.min-night

``` {code-block} python
html_style = 'css/bulma.min-night.css'
```

![Bulma Night](_static/_images/bulma.min-night.png)

### Bulma.min-red

``` {code-block} python
html_style = 'css/bulma.min-red.css'
```

![Bulma Red](_static/_images/bulma.min-red.png)

Adding your own css
-------------------

You can always add more stylesheets to the already provided stylesheets
by visiting [Bulmaswatch](https://jenil.github.io/bulmaswatch/) . Just
download the style and give a shoutout to bulma afterwards on
[Twitter](https://twitter.com/) .

Add the css file to `static/css` and change the html\_style to the given
name.
