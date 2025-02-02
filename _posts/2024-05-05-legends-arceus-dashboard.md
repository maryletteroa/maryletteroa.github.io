---
layout: post
title: Pokemon Legends Arceus Dashboard
categories: [project]
tags: [powerbi]
image:
  path: /assets/images/legends-arceus-dashboard/summary.png
---

Here's a quick follow up to the [first Pokemon dashboard]({% link _posts/2024-04-20-pokemon-dashboard (first generation).md %}) I've made. (I keep doing this because this has been so much fun for me 😁). I discussed some aspects about the game in this post so 📢 SPOILER ALERT! up ahead.

I've finally picked up **Pokemon Legends: Arceus** in the Nintendo Switch. This game was released in 2022 and is the first Pokemon game that features an open world. (I'm a big fan of *Zelda: Breath of the Wild* and this game kind of reminds me of that). 

<center><img src="https://upload.wikimedia.org/wikipedia/en/9/9c/Pokemon_Legends_Arceus_cover.jpg" alt="legends-arceus" width="250"/><small>Photo Credit: Wikipedia</small></center>

The game is set in the past (or is it another dimension?) wherein Pokemons are not yet well-understood. This made for an interesting gameplay with the player discovering details about each of the Pokemons and contributing to research along the way. The battle mechanism has also been refreshed with the addition of strong and agile move styles. What I liked the most is the "organic" way in which a player encounters Pokemons in the wild (although, it's still kind of annoying to be attacked by wild Pokemons all of sudden - that part hasn't changed). The Pokemons are also rendered proportional to their size which makes for better immersion. 

<center><img src="https://progameguides.com/wp-content/uploads/2022/01/pokemon-legends-arceus-volo.jpg?w=1200" alt="volo" width="250"/><small>Photo Credit: Pro Game Guides / The Pokemon Company</small></center>

I was hooked for several days and made straigth progress in the main storyline (I've reached the credit roll on Day 3 or 4). However, I got a bit demotivated because my favorite character turned out to be a villain. (Is there a redemption arc for him? I haven't finished the battle yet). It was also becoming increasingly apparent, since I've booked it in the main quests, that I've neglected leveling up my Pokemons or exploring much of the Hisui region. I haven't played Pokemon in a long while and is out of the loop with the more recent generations. So whenever a Pokemon comes up in a side-quest for example, it's literally "Who's that Pokemon" for me. 

<center><img src="/assets/images/legends-arceus-dashboard/whos-that-pokemon.png" alt="whos-that-pokemon.png" width="250"/><small>Photo Credit: Pro Game Guides / The Pokemon Company</small></center>

Since I've made a Pokemon dashboard before [inspired by Fire Red](https://maryletteroa.github.io/blog/2024/04/20/pokemon-dashboard-(first-generation).html), I thought why not try an exclusive dashboard for Legends: Arceus. 

I also got insipired by this build [Who’s that Pokemon](https://www.linkedin.com/feed/update/urn:li:activity:7191116307323346944/). It’s miles away from what I’m capable of, I’m afraid, but one thing that made quite an impression on me is the Evolution Chart. I thought it could be an interesting challenge to set that up for the next Pokemon Dashboard. I also wanted to revisit the PowerBI model, specially improve the many-to-many relationships between Pokemons and moves, types, or abilities.

Here's how I did it.

First, I've looked up the [Poke API](https://pokeapi.co/) again and saw that it will be challenging to pick out all the Pokemons by which game they appeared. Fortunately, there is a [Pokedex endpoint](https://pokeapi.co/docs/v2#pokedexes) which has an entry for Hisui. It lists out all the Pokemons in that region, which totals (spoiler!) 242. (Spoiler for me also, but no matter, it's not like I've finished a Pokedex before.)

Next, (and this is the bit which I haven't understood entirely yet), I checked out the [evolution chain enpoint](https://pokeapi.co/docs/v2#evolution-section). To make it simple, I thought to get only those evolution paths that are in a "straight" line, example Charmander evolves to Charmeleon evolves to Charizard, and only part of the the branching ones e.g. Eevee can evolve to Vaporeon or Flareon or Jolteon.

I then started writing a script and tried out [Pokebase](https://github.com/PokeAPI/pokebase), a wrapper library for the Poke API in Python, but then found out it takes too long for me, and so I recycled  the [other Pokemon dataset scripts](https://github.com/maryletteroa/pokemon-dataset) I've written previously. One difference in the extraction compared to the first one is that I didn't break out the lists of types, moves, and abilities, and instead delegated much of the transformation to PowerQuery in PowerBI. 

I also found this webpage, [PokemonDB for Legends Arceus](https://pokemondb.net/pokedex/game/legends-arceus), that is a good reference to double check and/or understand the data.

Here's how the Legends Arceus dashboard looks so far: 

<center><img src="/assets/images/legends-arceus-dashboard/summary.png" alt="summary-page" width="500"/></center>

The summary page contains the top Pokemon based on stats (I didn't expect Electrode to be in there but - spoiler - Arceus is), some charts on the distribution of type, shapes, habitats, and legendary Pokemons which also serve as other ways to filter the data.

<center><img src="/assets/images/legends-arceus-dashboard/details.png" alt="details-page" width="500"/></center>

Just like the first dashboard, I made a drill through page with all the other stats and details of a Pokemon. I've also updated the gauge charts with dynamic traffic lights to better visually portray how a Pokemon stands with the rest of the group. The details page also contains the Evolution chain! Quite proud of myself there as it was a bit of challenge to plan and setup.

<center><img src="/assets/images/legends-arceus-dashboard/model.png" alt="model" width="500"/></center>

For the model, I included bridge tables to handle the many to many relationships between Pokemons and types, move, or abilities. I also made more transformations in PowerQuery to clean and set up the tables. My favorite is Merge Queries which I used to get details for the evolution table - that way, I don't have to rely too much on DAX and so actually made less calculations in Arceus dashboard than the Fire Red one. 

Here's the Pokemon I *dislike* the most in the game (strong sentiments, lol).

<center><img src="/assets/images/legends-arceus-dashboard/giratina.png" alt="giratina" width="500"/></center>

I wasn't able to pull out data in some of the Pokemons so the details page look empty. (The UX in these cases are not well polished.)

The most adorbs Pokemon in all of Hisui:

<center><img src="/assets/images/legends-arceus-dashboard/togepi.png" alt="togepi" width="500"/></center>

Finally has data on Togepi and it's one of the first Pokemons I've encountered (and battled!) in the game.

And this too! I don't know who this is, I've just discovered this Pokemon in this dashboard lol.

<center><img src="/assets/images/legends-arceus-dashboard/turtwig.png" alt="turtwig" width="500"/></center>

I can think of more ways to improve this. For example, I have not put in the stats filter, or details about the moves, or delved into more analysis (the top stats could change once the missing datapoints are filled), and still have not figured out the whole Evolution Chain entirely. But I was able to setup the Evolution Chain visualization and improved the model, so I'm quite happy. 😊

So, this is it for now. I might check out the other recent Pokemon games in the future but Pokemon Legends: Arceus is already so good and innovative, I really enjoyed playing this game, and amazed at how it's been designed and written.

The scripts repository is here: [pokemon-legends-arceus-dataset](https://github.com/maryletteroa/pokemon-legends-arceus-dataset)

And here is the dashboard! (Open in full screen)

<iframe title="legends-arceus" width="600" height="373.5" src="https://app.powerbi.com/view?r=eyJrIjoiNmRiMzlmNTgtMWU2Ni00ZDJkLTlmMmItZWZjNWU1OWVmNzA5IiwidCI6Ijg4NWVhN2NiLWQ4YjUtNGQ2Ni1hNGRjLTQ0MDM5MzcwM2FjMCIsImMiOjEwfQ%3D%3D" frameborder="0" allowFullScreen="true"></iframe>

<small>
Log:<br>
-2024-05-05 Initial version of the dashboard as described in this post
</small>