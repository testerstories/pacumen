## Pacumen

The name of this project is based on the name "Pac-Man" and the word "acumen." The term generally refers to the ability to make good judgments and quick decisions. This is often done in a particular domain.

To that end, **Pacumen** is an implementation of the [Pacman AI project](http://ai.berkeley.edu) developed at UC Berkeley. This is a project that allows you to provide customized Pac-Man variations and then apply learning algorithms to those variations. I'm using this project as part of my studies into reinforcement learning as well as a means by which to get software test specialists up to speed on how to consider quality when testing in such a context.

In terms of the Berkeley AI code, it's a bit of a nightmare of poor coding in many ways. My plan is to modify a lot of the existing code to make it more in line with good Python coding practices as well as make it more modular and thus easier to maintain.

One of my original plans was to update the code to run on Python 3. **Currently Pacumen requires the Python 2.x branch.** The main complication for conversion is the heavy usage of Tkinter. The benefit of this has been not having to use external graphics libraries. The downside is that the changes between Tkinter between Python 2 and 3 are annoying to work with when you just want to get something done.
